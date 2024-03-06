import React from 'react';
import { Table } from 'antd';

const ScanTable = ({ columns, scanResults, pageSize }) => {
    return (
        <Table columns={columns} dataSource={scanResults} pagination={{ pageSize }} />
    );
};

export default ScanTable;
