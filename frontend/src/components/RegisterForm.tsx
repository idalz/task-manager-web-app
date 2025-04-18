import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const RegisterForm = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.post('/api/signup', {
        email,
        password,
      });

      if (response.status === 201 || response.status === 200) {
        setSuccess('Account created successfully!');
        setError('');
        setTimeout(() => {
          navigate('/'); // Redirect to login page
        }, 1500);
      }
    } catch (err: any) {
      setSuccess('');
      if (err.response?.status === 400) {
        setError('Email already registered.');
      } else {
        setError('Something went wrong. Please try again.');
      }
    }
  };

  return (
    <div className="register-form">
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <button type="submit">Register</button>
        </div>
      </form>
      <div>
        <span>Already have an account? <a href="/">Login here</a></span>
      </div>
    </div>
  );
};

export default RegisterForm;
