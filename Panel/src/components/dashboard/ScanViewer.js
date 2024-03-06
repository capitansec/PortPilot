import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Descriptions, Spin, Collapse, Button } from 'antd';
import {
    ClockCircleOutlined,
    UserOutlined,
    DesktopOutlined,
    UnorderedListOutlined,
    CheckCircleOutlined,
    ExclamationCircleOutlined,
} from '@ant-design/icons';

const { Panel } = Collapse;

const ScanViewer = () => {
    const { uuid } = useParams();
    const [scanDetails, setScanDetails] = useState(null);

    useEffect(() => {
        const fetchScanDetails = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BASE_URL}/v2/result/${uuid}`, {
                    headers: {
                        'accept': 'application/json',
                        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });

                setScanDetails(response.data);
            } catch (error) {
                console.error('Error fetching scan details:', error);
            }
        };

        fetchScanDetails();
    }, [uuid]);

    if (!scanDetails) {
        return <Spin tip="Loading..." />;
    }

    const scan = scanDetails.result.scans[0];

    return (
        <div className="bas">
            <h2>
                <DesktopOutlined style={{ marginRight: '10px' }} />
                Scan Details for UUID: {uuid}
            </h2>
            <hr />
            <br />

            <Descriptions title="Scan Information" bordered column={1}>
                <Descriptions.Item label="Scan Name">
                    <UnorderedListOutlined style={{ marginRight: '10px' }} />
                    {scan.scan_name}
                </Descriptions.Item>
                <Descriptions.Item label="Scan Owner">
                    <UserOutlined style={{ marginRight: '10px' }} />
                    {scan.scan_owner}
                </Descriptions.Item>
                <Descriptions.Item label="Scan Date and Time">
                    <ClockCircleOutlined style={{ marginRight: '10px' }} />
                    {new Date(scan.scan_datetime).toLocaleString()}
                </Descriptions.Item>
                <Descriptions.Item label="Scanned Host">
                    <DesktopOutlined style={{ marginRight: '10px' }} />
                    {scan.host}
                </Descriptions.Item>
            </Descriptions>

            <div style={{ marginTop: '20px' }}>
                <br />
                <h3 style={{ color: '#52c41a' }}>
                    <CheckCircleOutlined style={{ marginRight: '10px', color: '#52c41a' }} />
                    Open Ports
                </h3>
                <br />
                <Collapse accordion>
                    <Panel
                        header={
                            <span>
                                <UnorderedListOutlined style={{ marginRight: '10px' }} />
                                Click to see open ports
                            </span>
                        }
                        key="1"
                    >
                        <ul>
                            {scan.open_ports.map(port => (
                                <li key={port}>{port}</li>
                            ))}
                        </ul>
                    </Panel>
                </Collapse>
            </div>

            <Button type="primary" style={{ marginTop: '20px' }} onClick={() => window.history.back()}>
                Back
            </Button>
        </div>
    );
};

export default ScanViewer;
