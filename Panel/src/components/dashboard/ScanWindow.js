import React, {useState} from 'react';
import {Button, Input, message} from 'antd';
import axios from 'axios';
import {LockOutlined, UserOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import logo from "../../assets/logo.png";

const ScanWindow = ({onScanComplete}) => {
    const BASE_URL = process.env.REACT_APP_BASE_URL;
    const [scanData, setScanData] = useState({
        scanName: '',
        scanOwner: '',
        target: '',
    });

    const handleInputChange = (key, value) => {
        setScanData((prevData) => ({...prevData, [key]: value}));
    };

    const handleScan = async () => {
        try {
            const {scanName, scanOwner, target} = scanData;
            const response = await axios.post(
                BASE_URL + '/v2/scan',
                {
                    scan_id: generateUUID(), // You can use a function to generate UUID
                    scan_name: scanName,
                    scan_owner: scanOwner,
                    target: target,
                    request_datetime: new Date().toISOString(),
                },
                {
                    headers: {
                        accept: 'application/json',
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                }
            );

            if (response.data === 'sent') {
                message.success('Scan request has been successfully sent.');
                onScanComplete(); // Notify the parent component that the scan is complete
            }
        } catch (error) {
            console.error('Error sending scan request:', error);
            message.error('Error sending scan request. Please try again.');
        }
    };

    // Function to generate UUID
    const generateUUID = () => {
        // Implement your UUID generation logic here
        // You can use an external library or create a simple one
        // For example, you can refer to: https://www.uuidgenerator.net/version4
    };

    return (
        <section>
            <div className='wrapper'>

                <h1 style={{color: 'white'}}>Login</h1>
                <form>
                    <div className='input-box'>
                        <input
                            type="text"
                            placeholder='Host to scan'
                            id='Host To Scan'
                            autoComplete='off'
                            value="Host To Scan"
                        />
                    </div>


                    <div className='input-box'>
                        <input
                            type="text"
                            placeholder='Scan Owner'
                            id='scan_owner'
                            autoComplete='off'
                            value="Scan Owner"
                        />
                    </div>

                    <div className='input-box'>
                        <input
                            type="text"
                            placeholder='scan_name'
                            id='scan_name'
                            autoComplete='off'
                            value="Scan Name"
                        />
                    </div>


                    <button id="scan-btn">
                        Scan
                    </button>

                </form>


            </div>
        </section>
    );
};

export default ScanWindow;
