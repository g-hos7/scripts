/*
Tim Barnes
v1.1.0
2022-07-21

A Google Apps Script designed to manage my gmail inbox. The script checks the
time received of all messages in my inbox. If the time falls outside of my predefined
business hours, the message is archived and marked as read to suppress notifications
and an "After Hours" label is applied so that I can see what I missed every weekday
morning.
*/

function MoveMsgBasedOnTime() 
{
  //If during business hours, exit early
  if (WorkHours() == true)
  {
    return;
  }

  var label = GmailApp.getUserLabelByName("After Hours")
  var Threads = GmailApp.getInboxThreads();

  for (var i = 0; i < Threads.length; i++) 
  {
    var Msgs = Threads[i].getMessages();
    for (var j=0;j < Msgs.length ;j++)
    {
      var MsgTime = Msgs[j].getDate();
      //Sunday = 0, Saturday = 6
      if (MsgTime.getDay() == 0 || MsgTime.getDay() == 6)
      {
        //Silence notifications and apply label
        Threads[i].moveToArchive();
        Threads[i].markRead();
        Threads[i].addLabel(label);
      }

      if (MsgTime.getDay() == 1 || MsgTime.getDay() == 2 || MsgTime.getDay() == 3 || MsgTime.getDay() == 4 || MsgTime.getDay() == 5 )
      {
        var startTime = '7:00 AM';
        var endTime   = '4:00 PM';
        var startDate = dateObj(startTime,MsgTime);
        var endDate   = dateObj(endTime,MsgTime);

        var actionToTake = MsgTime < endDate && MsgTime > startDate ? 'continue' : 'silence';

        if (actionToTake == 'silence')
        {
            Threads[i].moveToArchive();
            Threads[i].markRead();
            Threads[i].addLabel(label);
        }
      }
    }
  }
}

function WorkHours()
{
  var date = new Date();
  var weekday = date.toLocaleString("en-US", {
    timeZone: "America/Chicago",
    weekday: 'long'
  })
  var start = 700;
  var end = 1600;
  const options = 
  {
    timeZone: 'America/Chicago',
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
  };
  time = date.toLocaleTimeString('en-US', options);
  time = Number(time.replace(':', ''));

  if ((weekday!="Saturday" && weekday!="Sunday") && (time >= start && time <= end))
  {
    return true;
  } else {
    return false;
  }
}


function dateObj(d,MsgTime) 
{
  var parts = d.split(/:|\s/),
      date  = new Date(MsgTime);
  if (parts.pop().toLowerCase() == 'pm') parts[0] = (+parts[0]) + 12;
  date.setHours(+parts.shift());
  date.setMinutes(+parts.shift());
  return date;
}