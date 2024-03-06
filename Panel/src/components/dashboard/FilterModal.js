import React, { useState } from 'react';
import { Modal, Form, Input, Button } from 'antd';

const FilterModal = ({ isModalVisible, handleOk, handleCancel, applyFilters }) => {
    const [form] = Form.useForm();

    const onFinish = (values) => {
        applyFilters(values);
        handleOk();
    };

    return (
        <Modal
            title="Filter Scans"
            visible={isModalVisible}
            onOk={handleOk}
            onCancel={handleCancel}
            footer={[
                <Button key="back" onClick={handleCancel}>
                    Cancel
                </Button>,
                <Button key="submit" type="primary" onClick={form.submit}>
                    Apply Filters
                </Button>,
            ]}
        >
            <Form form={form} onFinish={onFinish}>
                <Form.Item label="Scan Name" name="scanName">
                    <Input placeholder="Enter scan name" />
                </Form.Item>
                <Form.Item label="Scan Owner" name="scanOwner">
                    <Input placeholder="Enter scan owner" />
                </Form.Item>
                <Form.Item label="Datetime" name="datetime">
                    <Input placeholder="Enter datetime" />
                </Form.Item>
                <Form.Item label="Host" name="host">
                    <Input placeholder="Enter host" />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default FilterModal;
