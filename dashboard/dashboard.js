Jobs = new Mongo.Collection("jobs");

MyLineChart = null;

if (Meteor.isClient) {
  // This code only runs on the client
  Template.jobs.helpers({
    jobs: function () {
      return find_jobs();
    }
  });

  Template.stats.helpers({
      unclaimed_count: function() {
            return find_jobs().filter(
              function(o, index ) {
                return o.status === "UNCLAIMED";
              }).length;
      },
      claimed_count: function() {
            return find_jobs().filter(
              function(o, index ) {
                return o.status === "CLAIMED";
              }).length;
      },
      complete_count: function() {
            return find_jobs().filter(
              function(o, index ) {
                return o.status === "COMPLETE";
              }).length;
      }
  });

  $(function() {
    //drawChart();
  });

  Tracker.autorun(function () {
    //drawChart();
  });

}

function find_jobs(){
  var jobs = Jobs.find({}, {sort: {_id: -1}, limit: 1});

  if (jobs){
    result = jobs.fetch()[0];
    if (result){
      result = result.jobs;
    }
  }
  else{
    result = [];
  }
  return result;
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
  });
}


