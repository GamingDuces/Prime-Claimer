import React from 'react';

function Tutorial({ onFinish }) {
  return (
    <div>
      <h2>Welcome to Prime Claimer!</h2>
      <p>We will guide you through the first steps...</p>
      <button onClick={onFinish}>Finish Tutorial</button>
    </div>
  );
}

export default Tutorial;
// This component is a simple tutorial page that welcomes the user and provides a button to finish the tutorial.