import React, { useState } from 'react';
import { Menu, Dropdown, Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import './Dashboard.css';
import Users from './components/dashboard/Users';
import Scans from './components/dashboard/Scans';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [activeComponent, setActiveComponent] = useState('scans'); // Default to 'scans'

  const handleLogout = async () => {
    try {
      const response = await axios.get('http://localhost:8000/v1/user/logout', {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        },
      });
  
      if (response.data.status === 'success') {
        console.log('User logged out successfully');
      } else {
        console.error('Error logging out:', response.data.message);
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  
    sessionStorage.removeItem('token');
    dispatch({ type: 'LOGOUT' });
    navigate("/dashboard");
  };

  const menu = (
    <Menu>
      <Menu.Item key="1" onClick={handleLogout}>
        Logout
      </Menu.Item>
    </Menu>
  );

  return (
    <div className='wrapper2'>
      <Menu mode="horizontal" theme="dark" style={{marginBottom: '60px'}}>
        <Menu.Item key="1" onClick={() => setActiveComponent('scans')}>
          <h3>Scans</h3>
        </Menu.Item>
        <Menu.Item key="2" onClick={() => setActiveComponent('users')}>
          <h3>Users</h3>
        </Menu.Item>
        <Menu.Item key="3" onClick={() => setActiveComponent('status')}>
          <h3>Status</h3>
        </Menu.Item>
        <Menu.Item id='tester' key="4" style={{ float: 'right' }}>
          <Dropdown overlay={menu}>
            <Avatar size={64} icon={<UserOutlined />} style={{ fontSize: '18px', fontWeight: 'bold' }} />
          </Dropdown>
        </Menu.Item>
      </Menu>

      {activeComponent === 'scans' && <Scans />}
      {activeComponent === 'status' && <Scans />}
      {activeComponent === 'users' && <Users />}
    </div>
  );
};

export default Dashboard;
