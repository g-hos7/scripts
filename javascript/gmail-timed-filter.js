/*
Tim Barnes
v2.1.0
2022-07-21

A Google Apps Script designed to manage my gmail inbox. The script checks the
timestamp of each message in my inbox. If the timestamp falls outside of my
predefined business hours, the message is archived, marked as read, and an
"After Hours" label is applied to supress notifications and collect everything
missed during off hours.
*/

const clockInTime = 700;
const clockOutTime = 1600;
const today = new Date();
const timezone = 'America/Chicago';
const locale = 'en-US';
const daysOff = ['Saturday', 'Sunday'];
const label = GmailApp.getUserLabelByName("After Hours")

function main() 
{
  if (isItBusinessHours())
  {
    return;
  } else {
    let threads = GmailApp.getInboxThreads();

    for (let i = 0; i < threads.length; i++) 
    {
      let messages = threads[i].getMessages();

      for (let j = 0; j < messages.length; j++)
      {
        let messageTimestamp = messages[j].getDate();
        let timeDelivered = getTimeDelivered(messageTimestamp);
        let dayDelivered = getDayDelivered(messageTimestamp);

        if (daysOff.includes(dayDelivered))
        {
          handleMessage(threads[i]);
        } else if (timeDelivered <= clockInTime || timeDelivered >= clockOutTime) {
          handleMessage(threads[i]);
        }
      }
    }
    return;
  }
}

function isItBusinessHours()
{
  let weekday = today.toLocaleString(locale, {
    timeZone: timezone,
    weekday: 'long'
  });
  
  const options = 
  {
    timeZone: timezone,
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
  };
  let time = today.toLocaleTimeString(locale, options);
  time = Number(time.replace(':', ''));

  if (!daysOff.includes(weekday) && (time>=clockInTime && time<=clockOutTime))
  {
    return true;
  } else {
    return false;
  }
}

function getTimeDelivered(timestamp)
{
  const options = {
    timeZone: timezone,
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
  };
  return Number(timestamp.toLocaleTimeString(locale, options));
}

function getDayDelivered(timestamp)
{
  const options = {
    timeZone: timezone,
    weekday: 'long'
  };
  return timestamp.toLocaleString(locale, options);
}

function handleMessage(thread)
{
  thread.moveToArchive();
  thread.markRead();
  thread.addLabel(label);
  return;
}