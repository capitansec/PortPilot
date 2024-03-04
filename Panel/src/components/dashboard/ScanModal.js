// ScanModal.js
import React from 'react';
import { Modal, Form, Input, Button } from 'antd';

const ScanModal = ({ isModalVisible, handleOk, handleCancel, formData, setFormData, sendScanRequest }) => {
    return (
        <Modal
            title="Scan Request"
            visible={isModalVisible}
            onOk={handleOk}
            onCancel={handleCancel}
        >
            <Form>
                <Form.Item
                    label="Scan Name"
                    name="scanName"
                    rules={[
                        {
                            required: true,
                            message: 'Please input scan name!',
                        },
                    ]}
                >
                    <Input
                        onChange={(e) => setFormData({ ...formData, scanName: e.target.value })}
                        value={formData.scanName}
                    />
                </Form.Item>

                <Form.Item
                    label="Ip Address"
                    name="ipAddress"
                    rules={[
                        {
                            required: true,
                            message: 'Please input your username!',
                        },
                    ]}
                >
                    <Input
                        onChange={(e) => setFormData({ ...formData, ipAddress: e.target.value })}
                        value={formData.ipAddress}
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default ScanModal;
