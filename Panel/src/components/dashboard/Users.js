import React, { useState, useEffect } from 'react';
import './Scans.css';
import { Button, Input, Table, Tag } from 'antd';
import axios from 'axios';
import { Pagination } from 'antd';

const pageSize = 7;

const Users = () => {
  const [userData, setUserData] = useState([]);
  const [searchUsername, setSearchUsername] = useState('');
  const [filteredUserData, setFilteredUserData] = useState([]);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/v1/users', {
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          },
        });

        if (response.data.status === 'success') {
          setUserData(response.data.result);
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, []);

  const handleSearch = () => {
    const filteredData = userData.filter(user =>
      user.username.toLowerCase() === searchUsername.toLowerCase()
    );
    setFilteredUserData(filteredData);
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'UUID',
      dataIndex: 'uuid',
      key: 'uuid',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
    },
  ];

  return (
    <>
      <div className='base'>
        <div className='input-box'>
          <Input
            style={{
              backgroundColor: 'rgba(240, 248, 255, 0.5)'
            }}
            type="text"
            placeholder='Username'
            id='ip-box'
            value={searchUsername}
            onChange={(e) => setSearchUsername(e.target.value)}
          />
          <Button type="primary" onClick={handleSearch}>
            Search
          </Button>
        </div>

        <div className='table-content'>
          <Table columns={columns} dataSource={searchUsername ? filteredUserData : userData} pagination={{ pageSize }} />
        </div>
      </div>
    </>
  );
};

export default Users;
