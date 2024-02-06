import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './LoginForm';
import Register from './RegisterForm'
import Dashboard from './Dashboard';
import { Provider, useSelector, useDispatch } from 'react-redux';
import { createStore } from 'redux';

const initialState = {
  isLoggedIn: false,
  token: null,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isLoggedIn: true,
        token: action.payload.token,
      };
    default:
      return state;
  }
};

const store = createStore(reducer);

const App = () => {
  return (
    <Provider store={store}>
      <AppBody />
    </Provider>
  );
};

const AppBody = () => {
  const isLoggedIn = useSelector((state) => state.isLoggedIn);

  const dispatch = useDispatch();

  useEffect(() => {
    const storedToken = sessionStorage.getItem('token');

    if (storedToken) {
      dispatch({ type: 'LOGIN_SUCCESS', payload: { token: storedToken } });
    }
  }, [dispatch]);

  return (
    <Router>
      <div>
        <Routes>
          <Route
            path="/login"
            element={isLoggedIn ? <Navigate to="/dashboard" /> : <LoginForm />}
          />
          <Route path='/register' Component={Register} />
          <Route
            path="/dashboard"
            element={isLoggedIn ? <Dashboard /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
