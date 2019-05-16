import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogActions from '@material-ui/core/DialogActions';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Typography from '@material-ui/core/Typography';
import BarChart from '../charts/BarChart'
import Instruction from './InstructDrawer'
import MyCloud from './MyCloud'
import Divider from '@material-ui/core/Divider';

const DialogTitle = withStyles(theme => ({
  root: {
    borderBottom: `1px solid ${theme.palette.divider}`,
    margin: 0,
    padding: theme.spacing.unit * 2,
  },
  closeButton: {
    position: 'absolute',
    right: theme.spacing.unit,
    top: theme.spacing.unit,
    color: theme.palette.grey[500],
  },
}))(props => {
  const { children, classes, onClose } = props;
  return (
    <MuiDialogTitle disableTypography className={classes.root}>
      <Typography variant="h6">{children}</Typography>
      {onClose ? (
        <IconButton aria-label="Close" className={classes.closeButton} onClick={onClose}>
          <CloseIcon />
        </IconButton>
      ) : null}
    </MuiDialogTitle>
  );
});

const DialogContent = withStyles(theme => ({
  root: {
    margin: 0,
    padding: theme.spacing.unit * 2,
  },
}))(MuiDialogContent);

const DialogActions = withStyles(theme => ({
  root: {
    borderTop: `1px solid ${theme.palette.divider}`,
    margin: 0,
    padding: theme.spacing.unit,
  },
}))(MuiDialogActions);

class CustomizedDialogDemo extends React.Component {
  state = {
    open: false,
    top: false,
    left: false,
    bottom: false,
    right: false,
  };

  handleClickOpen = () => {
    this.setState({
      open: true,
    });
  };

  handleClose = () => {
    this.setState({ open: false });
    this.props.setModalData('cancel');
  };

  toggleDrawer = (side, open) => () => {
    this.setState({
      [side]: open,
    });
  };

  handleDrawer = (type) => {
    if (type === 'cancel') {
      this.setState({
        top: false
      });
    } 
  }

  render() {

    const { modalOpen, data, districtName, totalOffence } = this.props

    return (
      <div>
        <Instruction
          topVisible={this.state.top}
          setDrawer={this.handleDrawer}
        />

        <Dialog
          onClose={this.handleClose}
          aria-labelledby="customized-dialog-title"
          open={modalOpen}
        >
          <DialogTitle id="customized-dialog-title" onClose={this.handleClose}>
            District: {districtName}
          </DialogTitle>
          <DialogContent>
             <BarChart 
                chartData={data}
                totalOffence={totalOffence}
              />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.toggleDrawer('top', true)} color="primary">
              Instructions
            </Button>
          </DialogActions>
            <Divider light />
           {/* <MyCloud /> */}

        </Dialog>

      </div>
    );
  }
}

export default CustomizedDialogDemo;