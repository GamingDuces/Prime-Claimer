import React, { useState } from 'react';
import api from '../api';

function Tutorial({ onFinish }) {
  const steps = [
    (
      <div key="intro">
        <h2>Welcome to Prime Claimer!</h2>
        <p>This short tutorial will guide you through the basics.</p>
      </div>
    ),
    (
      <div key="accounts">
        <h2>Add your Amazon account</h2>
        <p>Visit the Accounts page and log in to Amazon to enable auto-claiming.</p>
      </div>
    ),
    (
      <div key="claim">
        <h2>Claim your first game</h2>
        <p>Head over to the Dashboard to see available games and claim them.</p>
      </div>
    )
  ];

  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const next = async () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
      return;
    }
    try {
      setLoading(true);
      await api.post('/me/tutorial-complete');
      onFinish();
    } catch (err) {
      console.error('Failed to finish tutorial', err);
      setError('Failed to save progress');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {steps[step]}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={next} disabled={loading}>
        {step < steps.length - 1 ? 'Next' : 'Finish'}
      </button>
    </div>
  );
}

export default Tutorial;
