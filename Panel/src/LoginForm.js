import React, { useState, useRef, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import logo from './assets/logo.png';
import { UserOutlined, LockOutlined } from '@ant-design/icons';



const LoginForm = () => {
  const BASE_URL = process.env.REACT_APP_BASE_URL;
  console.log(BASE_URL)
  console.log(process.env.REACT_APP_BASE_URL);

  //Initial objects
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  // Refs
  const userRef = useRef();
  const errRef = useRef();


  // Validators
  const [validName, setValidName] = useState(false);

  const [validPwd, setValidPwd] = useState(false);

  const [errMsg, setErrMsg] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    setErrMsg('');
  }, [username, password]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(BASE_URL + '/v1/user/login', {
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
                placeholder='Username'
                id='username'
                ref={userRef}
                autoComplete='off'
                value={username} 
                required
                onChange={(e) => setUsername(e.target.value)}
                aria-invalid={validName ? 'false' : 'true'}
              />
              <UserOutlined className='icon'/>
            </div>

           
            <div className='input-box'>
              <input 
                type="password"
                placeholder='Password'
                id='password'
                value={password}
                required
                onChange={(e) => setPassword(e.target.value)} 
                aria-invalid={validPwd ? 'false' : 'true'}
              />
              <LockOutlined className='icon'/>
            </div>

            
            <button>
              Login
            </button>
            <div className="login-link">
                <p>
                  Don't have an account? <Link to="/register">Register</Link>
                </p>
              </div>
          </form>
        

      </div>
    </section>
  );
};

export default LoginForm;
