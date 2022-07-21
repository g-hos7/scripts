/*
Tim Barnes
v2.0.0
2022-07-21

A Google Apps Script designed to manage my gmail inbox. The script checks the
timestamp of each message in my inbox. If the timestamp falls outside of my
predefined business hours, the message is archived, marked as read, and an
"After Hours" label is applied so that I can see what I missed every weekday
morning.
*/

function MoveMsgBasedOnTime() 
{
  //If during business hours, exit early
  if (WorkHours() == true)
  {
    return;
  } else {
    const startTime = 700;
    const endTime   = 1600;
    var label = GmailApp.getUserLabelByName("After Hours")
    var Threads = GmailApp.getInboxThreads();

    for (var i = 0; i < Threads.length; i++) 
    {
      var Msgs = Threads[i].getMessages();

      for (var j=0;j < Msgs.length ;j++)
      {
        var MsgTimeStamp = Msgs[j].getDate();
        var MsgTime = GetMsgTime(MsgTimeStamp);
        var MsgDay = GetMsgDay(MsgTimeStamp);

        if (MsgDay == "Saturday" || MsgDay == "Sunday")
        {
          MoveMsg(Threads[i], label);
        } else if (MsgTime <= startTime || MsgTime >= endTime) {
          MoveMsg(Threads[i], label);
        }
      }
    }
    return;
  }
}

function WorkHours()
{
  var date = new Date();
  var weekday = date.toLocaleString("en-US", {
    timeZone: "America/Chicago",
    weekday: 'long'
  })
  const start = 700;
  const end = 1600;
  const options = 
  {
    timeZone: 'America/Chicago',
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
  };
  var time = date.toLocaleTimeString('en-US', options);
  time = Number(time.replace(':', ''));

  if ((weekday!="Saturday" && weekday!="Sunday") && (time >= start && time <= end))
  {
    return true;
  } else {
    return false;
  }
}

function GetMsgTime(timestamp)
{
  const options = {
    timeZone: 'America/Chicago',
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
  };
  return Number(timestamp.toLocaleTimeString('en-US', options));
}

function GetMsgDay(timestamp)
{
  const options = {
    timeZone: "America/Chicago",
    weekday: 'long'
  };
  return timestamp.toLocaleString("en-US", options);
}

function MoveMsg(thread, label)
{
  thread.moveToArchive();
  thread.markRead();
  thread.addLabel(label);
  return;
}