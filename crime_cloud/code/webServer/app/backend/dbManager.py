from couchdb import client, design
import json
import operator
import sys



class DbOperation:
    def __init__(self,username, password, url, database):
        path = 'http://' + username + ':' + password + '@' + url
        print(path)
        self.couch = client.Server(path)
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
        self.hashtag_view()

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

    def query_aurin(self, id):
        doc = self.couch['aurin'][id]
        return doc

    def upload_aurin(self,file):
        f = open(file, 'r')
        doc = f.readline()
        db = self.couch['aurin']
        db[file] = doc 

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
            word = word.replace(/[\ |\~|\`|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?]/g,\"\");\n \
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
                        word = text[i].toLowerCase()\n"+self.keywords()+"{return}\n} if(doc.sentiment=='negative'){\n\
                            emit(['I','Melbourne',doc.location.code, doc.id, word],1) \n}} }}"

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


    def hashtag_view(self):
        map_fun = "function (doc) {\n\
  if(doc.location.code != ''){\n\
    if(doc.hashtage != ''){\n\
      for (var i=0; i < doc.hashtage.length; i++){\n\
        hash = doc.hashtage[i].toLowerCase()\n\
        hash = hash.replace(/[\ |\~|\`|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?]/g,\"\")\n\
        emit(['Hashtage',doc.location.code, hash, doc.location.code], 1);\n\
      }\n\
    }\n\
  }\n\
}"      
        view = design.ViewDefinition('query', 'count_hashtage', map_fun, '_count')
        view.sync(self.db)
    

    def run_view_function(self, viewfunction, view_group, level):
        return self.db.view('query/'+viewfunction, group=view_group, group_level=level)


    def resultConverter(self, viewfunction, level):
        result = self.run_view_function(viewfunction, True, level)
        result_dic = {}
        for r in result:
            result_dic.update({r.key[level-1]:{r.key[0]:r.value}})
        return result_dic

    def hashtage_rank(self):
        result = self.run_view_function('count_hashtage', True, 3)
        lga_list={}
        for r in result:
            if(r.value > 10):
                if(r.key[2]!="melbourne" and r.key[2]!="australia"):
                    if(r.key[1] in lga_list):
                        lga_list[r.key[1]].update({r.key[2]:r.value})
                    else:
                        lga_list.update({r.key[1]:{}})
        hash_list = {}
        for lga in lga_list:
            sorted_lsit = sorted(lga_list[lga].items(), reverse=True, key=operator.itemgetter(1))[0:10]
            temp = {}
            for element in sorted_lsit:
                temp.update({element[0]:element[1]})
            hash_list.update({lga:temp})
        return hash_list
    

# if __name__ == "__main__":
#     print(sys.argv)
#     db = DbOperation('admin','123456', 'localhost:5984', 'out_test' )
#     db.createViews()
    # db.upload_aurin('aurin_sydn_crime_2017.geojson')
#     # db.uploadRawData()
    # db.uploadRawData('aurin_sydn.geojson')
#     # path = sys.argv[3]
    # print(db.query_aurin('aurin_sydn_crime_2017.geojson'))
#     # db.uploadRawData(path)

   
    
        
                
        

