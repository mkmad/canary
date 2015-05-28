Tasks = new Mongo.Collection("tasks");

if (Meteor.isClient) {
  // This code only runs on the client

  Template.jobs.helpers({
    tasks: function () {
      return Tasks.find({});
    }
  });

  Template.stats.helpers({
      total_count: function() { return Tasks.find().count(); },
      pending_count: function() { return Tasks.find({status: "POSTED"}).count(); },
      active_count: function() { return Tasks.find({status: "CLAIMED"}).count(); },
      failed_count: function() { return Tasks.find({status: "FAILED"}).count(); }
  });

  
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
  });
}
