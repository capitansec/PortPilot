import React from 'react';
import { Menu, Dropdown, Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import './Dashboard.css';
import Scans from './components/dashboard/Scans';


const Dashboard = () => {
  const handleLogout = () => {
    sessionStorage.removeItem()
    console.log("Logout");
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
      <Menu mode="horizontal" theme="dark">
        <Menu.Item key="1"><h3>Scans</h3></Menu.Item>
        <Menu.Item key="2"><h3>Status</h3></Menu.Item>
        <Menu.Item key="3"><h3>Users</h3></Menu.Item>
        <Menu.Item id='tester' key="4" style={{ float: 'right' }}>
          <Dropdown overlay={menu}>
            <Avatar size={64} icon={<UserOutlined />} style={{ fontSize: '18px', fontWeight: 'bold' }} />
          </Dropdown>
        </Menu.Item>
      </Menu>

      <Scans ></Scans>


    </div>
  );
};

export default Dashboard;
