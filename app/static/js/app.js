// Initialize an OpenTok Session object
let session;
session = OT.initSession(apiKey, sessionId);

// Initialize a Publisher, and place it into the element with id="publisher"
var publisher = OT.initPublisher('publisher');

// Attach event handlers
session.on({

  // This function runs when session.connect() asynchronously completes
  sessionConnected: function(event) {
    // Publish the publisher we initialzed earlier (this will trigger 'streamCreated' on other
    // clients)
    session.publish(publisher, function(error) {
      if (error) {
        console.error('Failed to publish', error);
      }
    });
  },

  // This function runs when another client publishes a stream (eg. session.publish())
  streamCreated: function(event) {
    // Create a container for a new Subscriber, assign it an id using the streamId, put it inside
    // the element with id="subscribers"
    var subContainer = document.createElement('div');
    subContainer.id = 'stream-' + event.stream.streamId;
    document.getElementById('subscribers').appendChild(subContainer);

    // Subscribe to the stream that caused this event, put it inside the container we just made
    session.subscribe(event.stream, subContainer, function(error) {
      if (error) {
        console.error('Failed to subscribe', error);
      }
    });
  }

});

// Receive a message and append it to the history
var msgHistory = document.querySelector('#history');
session.on('signal:msg', function signalCallback(event) {
    var msg = document.createElement('p');
    msg.textContent = event.data;
    msg.className = event.from.connectionId === session.connection.connectionId ? 'mine' : 'theirs';
    msgHistory.appendChild(msg);
    msg.scrollIntoView();
});


// Text chat
var form = document.querySelector('#form');
var msgTxt = document.querySelector('#msgTxt');

// Send a signal once the user enters data in the form
form.addEventListener('submit', function submit(event) {
    event.preventDefault();

    session.signal({
    type: 'msg',
    data: msgTxt.value
    }, function signalCallback(error) {
        if (error) {
            console.error('Error sending signal:', error.name, error.message);
        } else {
            msgTxt.value = '';
        }
    });
});


function handleCallback(error) {
  if (error) {
    console.log("error: " + error.message);
  } else {
    console.log("callback success");
  }
}

// Connect to the Session using the 'apiKey' of the application and a 'token' for permission
session.connect(token, function(error) {
  if (error) {
    console.error('Failed to connect', error);
  }
});

let screenSharePublisher;
const startShareBtn = document.getElementById("startScreenShare");
const stopShareBtn = document.getElementById("stopScreenShare");

startShareBtn.addEventListener("click", event => {
  OT.checkScreenSharingCapability(response => {
    if (!response.supported || response.extensionRegistered === false) {
      alert("Screen sharing not supported");
    } else if (response.extensionInstalled === false) {
      alert("Browser requires extension");
    } else {
      // Share screen code
      screenSharePublisher = OT.initPublisher(
        "screen",
        {
          insertMode: "append",
          width: "100%",
          height: "100%",
          videoSource: "screen",
          publishAudio: true
        },
        handleCallback
      );
      session.publish(screenSharePublisher, handleCallback);
      // CSS classes when screen-sharing starts
      startShareBtn.style.display = 'none';
      stopShareBtn.style.display = 'inline';
      document.getElementById("screen").classList.add("pub-active");
    }
  });
});

stopShareBtn.addEventListener("click", event => {
  screenSharePublisher.destroy();
  // CSS classes when screen-sharing stops
  startShareBtn.style.display = 'initial';
  stopShareBtn.style.display = 'none';
  document.getElementById("screen").classList.remove("pub-active");
});