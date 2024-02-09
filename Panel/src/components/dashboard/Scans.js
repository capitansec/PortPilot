import React, { useState, useEffect } from 'react';
import './Scans.css';
import { Button, Input, Table, message } from 'antd'; 
import axios from 'axios';
import { Pagination } from 'antd';

const pageSize = 7;

const Scans = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [scanResults, setScanResults] = useState([]);

  const handleScan = async () => {
    try {
      const response = await axios.post('http://localhost:8000/v1/scan', {
        target: searchTerm, 
        comment: 'string',
      }, {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });
  
      if (response.data === 'İletildi') {
        message.success('Scan request has been successfully sent.');
        setSearchTerm(''); 
      }
    } catch (error) {
      console.error('Error sending scan request:', error);
      message.error('Error sending scan request. Please try again.'); 
    }
  };

  const handleScanResults = async () => {
    try {
      const response = await axios.get('http://localhost:8000/v1/result', {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        },
      });

      if (response.data.results) {
        setScanResults(response.data.results);
      }
    } catch (error) {
      console.error('Error fetching scan results:', error);
    }
  };

  const columns = [
    {
      title: 'IP',
      dataIndex: 'ip',
      key: 'ip',
    },
    {
      title: 'Port',
      dataIndex: 'port',
      key: 'port',
    },
    {
      title: 'State',
      dataIndex: 'state',
      key: 'state',
    },
    {
      title: 'Timestamp',
      dataIndex: '@timestamp',
      key: '@timestamp',
    },
  ];

  return (
    <>
      <div className='base'>
        <div className='input-box' >
          <input style={{marginRight: '20px'}}
            type="text"
            placeholder='IP or Hostname'
            id='ip-box'
            onChange={(e) => setSearchTerm(e.target.value)} 
            value={searchTerm} 
            required
          />
          <Button type="primary" danger style={{marginRight: '20px'}} onClick={handleScan}>
            Scan
          </Button>

          <Button type="primary" onClick={handleScanResults}>
            Refresh
          </Button>
        </div>

        <div className='table-content'>
          <Table columns={columns} dataSource={scanResults} pagination={{ pageSize }} />
        </div>
      </div>
    </>
  );
};

export default Scans;
