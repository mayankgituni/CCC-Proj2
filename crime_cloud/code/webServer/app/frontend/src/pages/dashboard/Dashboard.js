import React from "react";
import {
  Grid,
  LinearProgress,
  Select,
  OutlinedInput,
  MenuItem,
  withStyles,
} from "@material-ui/core";
import {
  ResponsiveContainer,
  ComposedChart,
  AreaChart,
  LineChart,
  Line,
  Tooltip,
  Area,
  PieChart,
  Pie,
  Cell,
  YAxis,
  XAxis
} from "recharts";

import Loader from '../maps/loader';

import Axios from 'axios';

import mock from "./mock";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";
import Dot from "../../components/Sidebar/components/Dot";

import Table from "./components/Table/Table";
import BigStat from "./components/BigStat/BigStat";

import CompChart from "./compositeChart"

const getRandomData = (length, min, max, multiplier = 10, maxDiff = 10) => {
  const array = new Array(length).fill();
  let lastValue;

  return array.map((item, index) => {
    let randomValue = Math.floor(Math.random() * multiplier + 1);

    while (
      randomValue <= min ||
      randomValue >= max ||
      (lastValue && randomValue - lastValue > maxDiff)
    ) {
      randomValue = Math.floor(Math.random() * multiplier + 1);
    }

    lastValue = randomValue;

    return { value: randomValue };
  });
};


const getMainChartData = () => {
  const resultArray = [];
  const tablet = getRandomData(35, 3500, 6500, 7500, 1000);
  const desktop = getRandomData(35, 1500, 7500, 7500, 1500);
  const mobile = getRandomData(35, 1500, 7500, 7500, 1500);

  for (let i = 0; i < tablet.length; i++) {
    resultArray.push({
      tablet: tablet[i].value,
      desktop: desktop[i].value,
      mobile: mobile[i].value
    });
  }

  return resultArray;
};



const mainChartData = getMainChartData();

const PieChartData = [
  { name: "Group A", value: 400, color: "primary" },
  { name: "Group B", value: 300, color: "secondary" },
  { name: "Group C", value: 300, color: "warning" },
  { name: "Group D", value: 200, color: "success" }
];

const Dashboard = ({ classes, theme, ...props }) => {
  return (
    <React.Fragment>
      <PageTitle title="Dashboard" button="Latest Reports" />
      <Grid container spacing={32}>
        {/* <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Visits Today"
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <div className={classes.visitsNumberContainer}>
              <Typography size="xl" weight="medium">
                12, 678
              </Typography>
              <LineChart
                width={55}
                height={30}
                data={[
                  { value: 10 },
                  { value: 15 },
                  { value: 10 },
                  { value: 17 },
                  { value: 18 }
                ]}
                margin={{ left: theme.spacing.unit * 2 }}
              >
                <Line
                  type="natural"
                  dataKey="value"
                  stroke={theme.palette.success.main}
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </div>
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <Typography color="textSecondary">Registrations</Typography>
                <Typography size="md">860</Typography>
              </Grid>
              <Grid item>
                <Typography color="textSecondary">Sign Out</Typography>
                <Typography size="md">32</Typography>
              </Grid>
              <Grid item>
                <Typography color="textSecondary">Rate</Typography>
                <Typography size="md">3.25%</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid> */}


        <Grid item sm={6}>
          <Widget
            title="Tweet Data Analysis"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <div className={classes.performanceLegendWrapper}>
              <div className={classes.legendElement}>
                <Dot color="warning" />
                <Typography
                  color="textSecondary"
                  className={classes.legendElementText}
                >
                  Melbourne
                </Typography>
              </div>
              <div className={classes.legendElement}>
                <Dot color="primary" />
                <Typography
                  color="textSecondary"
                  className={classes.legendElementText}
                >
                  Sydney
                </Typography>
              </div>
            </div>
            <div className={classes.progressSection}>
              <Typography
                size="md"
                color="textSecondary"
                className={classes.progressSectionTitle}
              >
                Melbourne Tweets
              </Typography>
              <LinearProgress
                variant="determinate"
                value={33.75}
                classes={{ barColorPrimary: classes.progressBar }}
                className={classes.progress}
              />
            </div>
            <Grid item>
                <Typography color="textSecondary">melbourne tweets</Typography>
                <Typography size="md">1559361</Typography>
              </Grid>
              <Grid item>
                <Typography color="textSecondary">sydney tweets</Typography>
                <Typography size="md">3060922</Typography>
            </Grid>
            {/* <div>
              <Typography
                size="md"
                color="textSecondary"
                className={classes.progressSectionTitle}
              >
                SDK
              </Typography>
              <LinearProgress
                variant="determinate"
                value={30.60922}
                classes={{ barColorPrimary: classes.progressBar }}
                className={classes.progress}
              />
            </div> */}
          </Widget>
        </Grid>
        <Grid item xs={6}>
          <Widget
            title="Server Overview"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <div className={classes.serverOverviewElement}>
              <Typography
                color="textSecondary"
                className={classes.serverOverviewElementText}
              >
               Instance Name: web_server1
              </Typography>
              {/* <div className={classes.serverOverviewElementChartWrapper}>
                <ResponsiveContainer height={50} width="99%">
                  <AreaChart data={getRandomData(10)}>
                    <Area
                      type="natural"
                      dataKey="value"
                      stroke={theme.palette.secondary.main}
                      fill={theme.palette.secondary.light}
                      strokeWidth={2}
                      fillOpacity="0.25"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div> */}
            </div>
            <div className={classes.serverOverviewElement}>
              <Typography
                color="textSecondary"
                className={classes.serverOverviewElementText}
              >
                Volumn Name: web_vol1
              </Typography>
              {/* <div className={classes.serverOverviewElementChartWrapper}>
                <ResponsiveContainer height={50} width="99%">
                  <AreaChart data={getRandomData(10)}>
                    <Area
                      type="natural"
                      dataKey="value"
                      stroke={theme.palette.primary.main}
                      fill={theme.palette.primary.light}
                      strokeWidth={2}
                      fillOpacity="0.25"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div> */}
            </div>
            <div className={classes.serverOverviewElement}>
              <Typography
                color="textSecondary"
                className={classes.serverOverviewElementText}
              >
                Size: 10g
              </Typography>
              {/* <div className={classes.serverOverviewElementChartWrapper}>
                <ResponsiveContainer height={50} width="99%">
                  <AreaChart data={getRandomData(10)}>
                    <Area
                      type="natural"
                      dataKey="value"
                      stroke={theme.palette.warning.main}
                      fill={theme.palette.warning.light}
                      strokeWidth={2}
                      fillOpacity="0.25"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div> */}
            </div>
            <Typography
                color="textSecondary"
                className={classes.serverOverviewElementText}
              >
                172.26.38.43
              </Typography>
          </Widget>
        </Grid>
        {/* <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget title="Revenue Breakdown" upperTitle className={classes.card}>
            <Grid container spacing={16}>
              <Grid item xs={6}>
                <ResponsiveContainer width="100%" height={144}>
                  <PieChart
                    margin={{ left: theme.spacing.unit * 2 }}
                  >
                    <Pie
                      data={PieChartData}
                      innerRadius={45}
                      outerRadius={60}
                      dataKey="value"
                    >
                      {PieChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={theme.palette[entry.color].main}
                        />
                      ))}
                    </Pie>
                  </PieChart>
                  </ResponsiveContainer>
              </Grid>
              <Grid item xs={6}>
                <div className={classes.pieChartLegendWrapper}>
                  {PieChartData.map(({ name, value, color }, index) => (
                    <div key={color} className={classes.legendItemContainer}>
                      <Dot color={color} />
                      <Typography style={{ whiteSpace: 'nowrap' }}>&nbsp;{name}&nbsp;</Typography>
                      <Typography color="textSecondary">
                        &nbsp;{value}
                      </Typography>
                    </div>
                  ))}
                </div>
              </Grid>
            </Grid>
          </Widget>
        </Grid> */}
        
        <Grid item xs={12}>
          <Widget>
              <CompChart width="100%" />
          </Widget>
        </Grid>

        {/* <Grid item xs={12}>
          <Widget>
              <TagCloud />
          </Widget>
        </Grid> */}
        {/* {mock.bigStat.map(stat => (
          <Grid item md={4} sm={6} xs={12} key={stat.product}>
            <BigStat {...stat} />
          </Grid>
        ))} */}
        {/* <Grid item xs={12}>
          <Widget
            title="Support Requests"
            upperTitle
            noBodyPadding
            bodyClass={classes.tableWidget}
          >
            <Table data={mock.table} />
          </Widget>
        </Grid> */}
      </Grid>
    </React.Fragment>
  );
};

const styles = theme => ({
  card: {
    minHeight: "100%",
    display: "flex",
    flexDirection: "column"
  },
  visitsNumberContainer: {
    display: "flex",
    alignItems: "center",
    flexGrow: 1,
    paddingBottom: theme.spacing.unit
  },
  progressSection: {
    marginBottom: theme.spacing.unit
  },
  progressTitle: {
    marginBottom: theme.spacing.unit * 2
  },
  progress: {
    marginBottom: theme.spacing.unit,
    backgroundColor: theme.palette.primary.main
  },
  pieChartLegendWrapper: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "flex-end",
    marginRight: theme.spacing.unit
  },
  legendItemContainer: {
    display: "flex",
    alignItems: "center",
    marginBottom: theme.spacing.unit
  },
  fullHeightBody: {
    display: "flex",
    flexGrow: 1,
    flexDirection: "column",
    justifyContent: "space-between"
  },
  tableWidget: {
    overflowX: "auto"
  },
  progressBar: {
    backgroundColor: theme.palette.warning.main
  },
  performanceLegendWrapper: {
    display: "flex",
    flexGrow: 1,
    alignItems: "center",
    marginBottom: theme.spacing.unit
  },
  legendElement: {
    display: "flex",
    alignItems: "center",
    marginRight: theme.spacing.unit * 2,
  },
  legendElementText: {
    marginLeft: theme.spacing.unit
  },
  serverOverviewElement: {
    display: "flex",
    alignItems: "center",
    maxWidth: "100%"
  },
  serverOverviewElementText: {
    minWidth: 145,
    paddingRight: theme.spacing.unit * 2
  },
  serverOverviewElementChartWrapper: {
    width: "100%"
  },
  mainChartBody: {
    overflowX: 'auto',
  },
  mainChartHeader: {
    width: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    [theme.breakpoints.only("xs")]: {
      flexWrap: 'wrap',
    }
  },
  mainChartHeaderLabels: {
    display: "flex",
    alignItems: "center",
    [theme.breakpoints.only("xs")]: {
      order: 3,
      width: '100%',
      justifyContent: 'center',
      marginTop: theme.spacing.unit * 3,
      marginBottom: theme.spacing.unit * 2,
    }
  },
  mainChartHeaderLabel: {
    display: "flex",
    alignItems: "center",
    marginLeft: theme.spacing.unit * 3,
  },
  mainChartSelectRoot: {
    borderColor: theme.palette.text.hint + '80 !important',
  },
  mainChartSelect: {
    padding: 10,
    paddingRight: 25
  },
  mainChartLegentElement: {
    fontSize: '18px !important',
    marginLeft: theme.spacing.unit,
  }
});

export default withStyles(styles, { withTheme: true })(Dashboard);