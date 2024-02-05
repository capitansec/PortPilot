import React, { useState, useRef, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import logo from './assets/logo.png'


const LoginForm = () => {
  //Initial objects
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  // Refs
  const userRef = useRef();
  const errRef = useRef();


  // Validators
  const [user, setUser] = useState('');
  const [validName, setValidName] = useState(false);

  const [pwd, setPwd] = useState('');
  const [validPwd, setValidPwd] = useState(false);

  const [errMsg, setErrMsg] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    setErrMsg('');
  }, [user, pwd]);

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8000/v1/user/login', {
        username,
        password,
      });

      const token = response.data.result;

      dispatch({ type: 'LOGIN_SUCCESS', payload: { token } });

      sessionStorage.setItem('token', token);

      navigate('/dashboard');

    } catch (error) {
      console.error('Login failed:', error.message);
      if (!error?.response) {
        setErrMsg('No Server Response');
      } else if (error.response?.status === 401) {
        setErrMsg('Invalid Credentials');
      } else {
        setErrMsg('Login Failed');
      }
      errRef.current.focus();
    }
  };

  return (

    <section>
      <div className='wrapper'>

        <p ref={errRef} className={errMsg ? 'errmsg' : 'offscreen'} aria-live="assertive">
          {errMsg}
        </p>

        <div className="logo-context">
          <img src={logo} alt="Logo" />
        </div>

          <h1 style={{ color: 'white' }}>Login</h1>

          <form onSubmit={handleLogin}>
            <div className='input-box'>
              <input 
                type="text"
                id='username'
                ref={userRef}
                autoComplete='off'
                value={username} 
                required
                onChange={(e) => setUsername(e.target.value)}
                aria-invalid={validName ? 'false' : 'true'}
              />
            </div>
            <br />
            <label>
              Password:
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
            <br />
            <button>
              Login
            </button>
          </form>
        

      </div>
    </section>
  );
};

export default LoginForm;
