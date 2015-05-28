Jobs = new Mongo.Collection("jobs");

if (Meteor.isClient) {
  // This code only runs on the client
  Template.jobs.helpers({
    jobs: function () {
      return find_jobs();
    }
  });

  Template.stats.helpers({
      unclaimed_count: function() { return find_jobs().length; },
      active_count: function() { return Jobs.find({status: "CLAIMED"}).count(); },
      failed_count: function() { return Jobs.find({status: "FAILED"}).count(); }
  });

}

function find_jobs(){
  var jobs = Jobs.find({}, {sort: {_id: -1}, limit: 1});

  if (jobs){
    result = jobs.fetch()[0].jobs;
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


