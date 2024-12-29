import React, { useState } from 'react';
import useStore from '../store';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { setUser } = useStore();
};

export default Login;