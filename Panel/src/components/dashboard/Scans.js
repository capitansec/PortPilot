// Scans.js
import React, { useState } from 'react';
import './Scans.css';
import ScanTable from './ScanTable';
import ScanModal from './ScanModal';
import FilterModal from "./FilterModal";
import { Button, Table, message } from 'antd';
import axios from 'axios';
import {PlusCircleFilled, PlusCircleOutlined, ReloadOutlined, SearchOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";

const pageSize = 7;

const Scans = () => {
    const BASE_URL = process.env.REACT_APP_BASE_URL;
    const [searchTerm, setSearchTerm] = useState('');
    const [scanResults, setScanResults] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [formData, setFormData] = useState({
        scanName: '',
        ipAddress: ''
    });
    const navigate = useNavigate();


    const showModal = () => {
        setIsModalVisible(true);
    };


    const handleOk = () => {
        sendScanRequest();
        setIsModalVisible(false);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const handleScanResults = async () => {
        try {
            const response = await axios.get(BASE_URL + '/v2/results', {
                headers: {
                    'accept': 'application/json',
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                },
            });

            if (response.data.status === 'success' && response.data.result && response.data.result.scans) {
                const formattedResults = response.data.result.scans.map(scan => ({
                    key: scan.scan_id,
                    uuid: <Link to={`/scans/${scan.scan_id}`}>{scan.scan_id}</Link>,
                    scan_owner: scan.scan_owner,
                    scan_name: scan.scan_name,
                    ip: scan.host,
                    datetime: scan.scan_datetime,
                }));

                setScanResults(formattedResults);
            }
        } catch (error) {
            console.error('Error fetching scan results:', error);
        }
    };



    const sendScanRequest = async () => {
        try {
            const response = await axios.post(BASE_URL + '/v2/scan', {
                scan_name: formData.scanName,
                target: formData.ipAddress,
            }, {
                headers: {
                    'accept': 'application/json',
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.data === 'sent') {
                message.success('Scan request has been successfully sent.');
                setSearchTerm('');
                setFormData({
                    scanName: '',
                    ipAddress: ''
                });
            }
        } catch (error) {
            console.error('Error sending scan request:', error);
            message.error('Error sending scan request. Please try again.');
        }
    };

    const columns = [
        {
            title: 'UUID',
            dataIndex: 'uuid',
            key: 'uuid',
        },
        {
            title: 'Scan Owner',
            dataIndex: 'scan_owner',
            key: 'scan_owner',
        },
        {
            title: 'Scan Name',
            dataIndex: 'scan_name',
            key: 'scan_name',
        },
        {
            title: 'IP',
            dataIndex: 'ip',
            key: 'ip',
        },
        {
            title: 'Datetime',
            dataIndex: 'datetime',
            key: 'datetime',
        },
    ];

    const [isFilterModalVisible, setIsFilterModalVisible] = useState(false);

    const showFilterModal = () => {
        setIsFilterModalVisible(true);
    };

    const handleFilterModalOk = () => {
        // Handle filter modal OK if needed
        setIsFilterModalVisible(false);
    };

    const handleFilterModalCancel = () => {
        setIsFilterModalVisible(false);
    };

   const applyFilters = async (filters) => {
    try {
        // Convert camelCase to snake_case
        const snakeCaseFilters = {};
        Object.keys(filters).forEach(key => {
            const snakeCaseKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
            snakeCaseFilters[snakeCaseKey] = filters[key];
        });

        const filteredFilters = Object.fromEntries(
            Object.entries(snakeCaseFilters).filter(([key, value]) => value !== '')
        );

        const response = await axios.get(BASE_URL + '/v2/results', {
            headers: {
                'accept': 'application/json',
                'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
            },
            params: filteredFilters, // From GPT
        });

        if (response.data.status === 'success' && response.data.result && response.data.result.scans) {
            const formattedResults = response.data.result.scans.map(scan => ({
                key: scan.scan_id,
                uuid: <Link to={`/scans/${scan.scan_id}`}>{scan.scan_id}</Link>,
                scan_owner: scan.scan_owner,
                scan_name: scan.scan_name,
                ip: scan.host,
                datetime: scan.scan_datetime,
            }));

            setScanResults(formattedResults);
        }
    } catch (error) {
        console.error('Error fetching filtered scan results:', error);
    }

    setIsFilterModalVisible(false);
};

    return (
        <>
            <div className='base'>
                <div className='input-box'>
                    <Button type="primary" style={{ marginRight: '20px', backgroundColor:"#6494aa" }} onClick={handleScanResults}>
                       <ReloadOutlined /> Refresh
                    </Button>

                    <Button type="primary" style={{ marginRight: "20px", backgroundColor:"#AE8799"}} onClick={showFilterModal}>
                        <SearchOutlined />Filter
                    </Button>


                    <Button type="primary" style={{ marginRight: "10px", backgroundColor:"#90A959"}} danger onClick={showModal}>
                        <PlusCircleOutlined />Create
                    </Button>
                </div>

                <div className='table-content'>
                    <ScanTable columns={columns} scanResults={scanResults} pageSize={pageSize} />
                </div>
                <ScanModal
                    isModalVisible={isModalVisible}
                    handleOk={handleOk}
                    handleCancel={handleCancel}
                    formData={formData}
                    setFormData={setFormData}
                    sendScanRequest={sendScanRequest}
                />

                <FilterModal
                    isModalVisible={isFilterModalVisible}
                    handleOk={handleFilterModalOk}
                    handleCancel={handleFilterModalCancel}
                    applyFilters={applyFilters}
                />
            </div>
        </>
    );
};

export default Scans;
