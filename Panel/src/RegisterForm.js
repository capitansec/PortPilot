import React, { useState, useRef, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import logo from './assets/logo.png';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { message } from 'antd';



const LoginForm = () => {
  const BASE_URL = process.env.REACT_APP_BASE_URL;


  //Message notification configuration
  const [messageApi, contextHolder] = message.useMessage();
  const success = () => {
    messageApi.open({
      type: 'success',
      content: 'This is a success message',
    });
  };
  const error = () => {
    messageApi.open({
      type: 'error',
      content: 'This is an error message',
    });
  };


  //Initial objects
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  // Refs
  const userRef = useRef();
  const errRef = useRef();


  // Validators
  const [validName, setValidName] = useState(false);

  const [validPwd, setValidPwd] = useState(false);
  

  const [errMsg, setErrMsg] = useState('');

  useEffect(() => {
    setErrMsg('');
  }, [username, password, email]);

  const handleRegister = async e => {
    e.preventDefault();
    try {
      const response = await axios.post(BASE_URL + '/v1/user/register', {
        username,
        password,
        email,
      });

      const result = response.data.status;
      if (result === 'success'){
        message.success('User has been created');
      }



      navigate('/login');

    } catch (error) {
      if (!error?.response) {
        message.error('No Server Response');
      } 
      
      else if(error.response.status == 400 && error.response.data.detail === 'Username or email already exists'){
        message.error('Username or email already exists')
      }

      else {
        message.error('Unsupported error');
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

          <h1 style={{ color: 'white' }}>Register</h1>

          <form onSubmit={handleRegister}>
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
                type="mail"
                placeholder='Mail'
                id='mail'
                value={email}
                required
                onChange={(e) => setEmail(e.target.value)} 
              />
              <MailOutlined className='icon'/>
            </div>

            <div className='input-box'>
              <input 
                type="password"
                placeholder='Password'
                id='password-valid'
                value={password}
                required
                onChange={(e) => setPassword(e.target.value)} 
                aria-invalid={validPwd ? 'false' : 'true'}
              />
              <LockOutlined className='icon'/>
            </div>

            
            <button>
              Register
            </button>
            <div className="login-link">
                <p>
                  Already have an account? <Link to="/login">Login</Link>
                </p>
              </div>
          </form>
        

      </div>
    </section>
  );
};

export default LoginForm;
