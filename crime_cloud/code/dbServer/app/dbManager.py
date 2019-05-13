from couchdb import client, design
import json

class DbOperation:
    def __init__(self,username, password, url, database):
        path = 'http://' + username + ':' + password + '@' + url
        self.db = self.connectDb(path, database)
        self.createViews()
        

    def connectDb(self, path, database):
        try:
            couch = client.Server(path)
            if database in couch:
                db = couch[database]
                print('Existing database')
                return db
            else:
                db = couch.create(database)
                print('Created a new database')
                return db
        except:
            print('Cannot connect to CouchDB!')
            exit(0)

    def keywords(self):
        try:
            f = open('keywordsList.txt','r')
            word = f.readline()
            equalCheck = 'word == "'
            condition = 'if (' + equalCheck + word.rstrip() + '"'
            word = f.readline()
        except:
            print('can not open the file')
        while len(word) != 0:
            condition = condition + '||' + equalCheck + word.rstrip() + '"'
            word = f.readline()
        condition = condition + ')'
        return condition

        

    def uploadRawData(self, raw_data):
        try:
            file=open(raw_data,'r')
            line = file.readline()
            count = 1
            while len(line) != 0:
                print("Inserting: {} ".format(count), end='\r')
                doc = json.loads(line)
                self.db.save(doc)
                line=file.readline()
                count += 1
            print('done!')
        except:
            print('can not open the file')

    def createViews(self):
        self.tweetsQueryViews()
        self.countWordsView()
        self.findWrathWordsView()
        self.groupTweetView()
        self.negative_withKeywordsView()
        self.positive_withKeywordsView()
        self.negative_withoutKeywordsView()

    def tweetsQueryViews(self):
        # map_fun = '''function (doc) {
        #     emit(doc.user.id, 
        #     {'user_id':doc.user.id,'tweet_id':doc.id,'hashtag':doc.entities.hashtags,'text':doc.text, 
        #     'time':doc.created_at, 'coordinates':doc.coordinates.coordinates});
        #     }'''
        map = "function (doc) {emit(doc.user.id, \n \
            {'user_id':doc.user.id,'tweet_id':doc.id,'hashtag':doc.entities.hashtags,'text':doc.text,\
'time':doc.created_at, 'coordinates':doc.coordinates.coordinates});}"
        view = design.ViewDefinition('query','get_tweet_info', map)
        view.sync(self.db)
        

    def countWordsView(self):
        map_fun = "function (doc) { \n \
        if(doc.text){ \n\
        var text = doc.text.split(' ') \n\
        for (i=0; i < text.length; i++){ \
        word = text[i].toLowerCase()\n" + self.keywords() + "{\n\
        emit(word,1)}}}}"
        # print(map_fun)
        view = design.ViewDefinition('query','count_words',map_fun,'_count')
        view.sync(self.db)

    def findWrathWordsView(self):
        map_fun = "function (doc) {\n\
    var words_list = []\n\
    if(doc.text){\n\
        var text = doc.text.split(' ')\n\
        for (i=0; i < text.length; i++){\n\
            word = text[i].toLowerCase()\n\
            word = word.replace(/[\ |\~|\`|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?]/g"");\n \
            word = word.trim()\n" + self.keywords() + "{\n words_list.push(word) }}\
            if (words_list.length > 0){\n\
                emit(doc.id,{'tweet_id':doc.id,'user_id':doc.user,'words list':words_list, 'sentiment':doc.sentiment})\n}\n}\n}"
        view = design.ViewDefinition('query', 'find_wrath_word', map_fun)
        view.sync(self.db)
    

    def groupTweetView(self):
        map_fun = "function (doc) {\n\
                if(doc.text){\n\
                    if(doc.location.code != ''){\n\
                    var text = doc.text.split(' ')\n\
                        for (i=0; i < text.length; i++){\n\
                            word = text[i].toLowerCase()\n"+self.keywords()+"{\nemit(['keywords','Melbourne',doc.location.code, doc.id, word],1);}}}}}"
                            
        view = design.ViewDefinition('query', 'group_tweet', map_fun, '_count')
        view.sync(self.db)

   

    def negative_withKeywordsView(self):
        map_fun = "function (doc) {\n\
                if(doc.location.code != ''){\n\
                    if(doc.text){\n\
                        var text = doc.text.split(' ')\n\
                        for (i=0; i < text.length; i++){\n\
                        word = text[i].toLowerCase()\n"+self.keywords()+"{\nif(doc.sentiment=='negative'){\n\
                            emit(['IE','Melbourne',doc.location.code, doc.id, word],1) \n}}}} }}"

        view = design.ViewDefinition('query', 'negative&withKeywords', map_fun, '_count')
        view.sync(self.db)

    def negative_withoutKeywordsView(self):
        map_fun = "function (doc) {\n\
                if(doc.location.code != ''){\n\
                    if(doc.text){\n\
                        var text = doc.text.split(' ')\n\
                        for (i=0; i < text.length; i++){\n\
                        word = text[i].toLowerCase()\n"+self.keywords()+"{}\n else{if(doc.sentiment=='negative'){\n\
                            emit(['I','Melbourne',doc.location.code, doc.id, word],1) \n}}}} }}"

        view = design.ViewDefinition('query', 'negative&withoutKeywords', map_fun, '_count')
        view.sync(self.db)

    def positive_withKeywordsView(self):
        map_fun = "function (doc) {\n\
                if(doc.location.code != ''){\n\
                    if(doc.text){\n\
                        var text = doc.text.split(' ')\n\
                        for (i=0; i < text.length; i++){\n\
                        word = text[i].toLowerCase()\n"+self.keywords()+"{\nif(doc.sentiment=='positive'){\n\
                            emit(['E','Melbourne',doc.location.code, doc.id, word],1) \n}}}} }}"

        view = design.ViewDefinition('query', 'positive&withKeywords', map_fun, '_count')
        view.sync(self.db)

    def run_view_function(self, viewfunction, view_group, level):
        return self.db.view('query/'+viewfunction, group=view_group, group_level=level)


    def resultConverter(self, viewfunction, level):
        result = self.run_view_function(viewfunction, True, level)
        result_dic = {}
        for r in result:
            result_dic.update({r.key[2]:{r.key[0]:r.value}})
        return result_dic
    


    

    #def get_tweet_info(self):
    #     result = self.db.view('query/get_tweet_info',group=True)
    #     return result

    # def get_count_words(self):
    #     return self.db.view('query/count_words', group=True)

    # def get_wrath_tweet(self):
    #     return self.db.view('query/find_wrath_word',  group=True)

    # def get_group_tweet(self, level=1):
    #     return self.db.view('query/group_tweet', group=True, group_level=level)

    # def get_neg_withoutWord(self):
    #     return self.db.view('query/negative&withoutKeywords', group=True, group_level=3)
