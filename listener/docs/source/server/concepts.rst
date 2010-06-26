Server side models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following describes the models that exist on the server side and their relationships.

Error
-------------------

The error that has been recorded by the incoming receiver.

Group
-------------------

A grouping of errors. Rather than dealing with individual errors, you might like to deal with groups. This is probably more advisable for tickets or tracking. When an error is written a signal is triggered. A default group method listens to this signal to place the error in a group. An error can only be in one group.

Project
-------------------

A website or group of websites collected into a project. A project will have one or more domains. When an error is written a signal is triggered. A default project method listens to this signal to place the error within the appropriate project. An error can only be in one project