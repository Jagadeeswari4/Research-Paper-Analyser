import React, { useState } from "react";
import { Mail, Lock, ArrowRight, User, Phone, Calendar, CheckCircle, AlertCircle } from "lucide-react";

const Login = ({ setPage }) => {
  const [showRegister, setShowRegister] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState("");
  const [registeredUsers, setRegisteredUsers] = useState([]);
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    phone: "",
    dob: ""
  });
  const [loginData, setLoginData] = useState({
    email: "",
    password: ""
  });

  const handleLogin = () => {
    // Check if user is registered
    const userExists = registeredUsers.find(
      user => user.email === loginData.email
    );

    if (!userExists) {
      setShowError("You haven't registered yet. Please create an account.");
      setTimeout(() => setShowError(""), 3000);
      return;
    }

    // Check if password matches
    if (userExists.password !== loginData.password) {
      setShowError("Incorrect password. Please try again.");
      setTimeout(() => setShowError(""), 3000);
      return;
    }

    // If everything is correct
    setShowError("");
    setPage("upload");
  };

  const handleRegister = () => {
    // Check if email already registered
    const emailExists = registeredUsers.find(
      user => user.email === formData.email
    );

    if (emailExists) {
      setShowError("This email is already registered. Please login.");
      setTimeout(() => setShowError(""), 3000);
      return;
    }

    // Check if password is at least 8 characters
    if (formData.password.length < 8) {
      setShowError("Password must be at least 8 characters long.");
      setTimeout(() => setShowError(""), 3000);
      return;
    }

    // Register the user
    setRegisteredUsers([...registeredUsers, {
      fullName: formData.fullName,
      email: formData.email,
      password: formData.password,
      phone: formData.phone,
      dob: formData.dob
    }]);

    console.log("Registered Users:", registeredUsers);
    
    // Show success message
    setShowSuccess(true);
    
    // After 2 seconds, go back to login with email pre-filled
    setTimeout(() => {
      setShowSuccess(false);
      setShowRegister(false);
      
      // Pre-fill login email with registered email
      setLoginData({
        email: formData.email,
        password: ""
      });
      
      // Reset registration form
      setFormData({
        fullName: "",
        email: "",
        password: "",
        phone: "",
        dob: ""
      });
      
      setShowError("");
    }, 2000);
  };

  const handleLoginInputChange = (e) => {
    const { name, value } = e.target;
    setLoginData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user types
    setShowError("");
  };

  const handleRegisterInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user types
    setShowError("");
  };

  return (
    <div className="login-page">
      <div className="login-card">
        {showSuccess ? (
          // Success Message
          <div style={{ textAlign: 'center', padding: '40px 20px' }}>
            <CheckCircle size={60} color="#4CAF50" />
            <h2 style={{ color: '#4CAF50', margin: '20px 0 10px', fontSize: '24px' }}>
              Account Created Successfully!
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px' }}>
              Your account has been registered. Redirecting to login...
            </p>
          </div>
        ) : (
          <>
            <h1>{showRegister ? "Create Account" : "Login"}</h1>
            
            {/* Error Message */}
            {showError && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '12px 15px',
                background: 'rgba(239, 68, 68, 0.15)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                borderRadius: '12px',
                color: '#fca5a5',
                fontSize: '14px'
              }}>
                <AlertCircle size={18} />
                <span>{showError}</span>
              </div>
            )}
            
            {showRegister ? (
              // Register Form
              <>
                {/* Full Name */}
                <div className="input-group">
                  <User className="icon" size={20} />
                  <input 
                    type="text" 
                    name="fullName"
                    placeholder="Full Name" 
                    value={formData.fullName}
                    onChange={handleRegisterInputChange}
                    required
                  />
                </div>

                {/* Email */}
                <div className="input-group">
                  <Mail className="icon" size={20} />
                  <input 
                    type="email" 
                    name="email"
                    placeholder="Email Address" 
                    value={formData.email}
                    onChange={handleRegisterInputChange}
                    required
                  />
                </div>

                {/* Password */}
                <div className="input-group">
                  <Lock className="icon" size={20} />
                  <input 
                    type="password" 
                    name="password"
                    placeholder="Password (min 8 characters)" 
                    value={formData.password}
                    onChange={handleRegisterInputChange}
                    required
                  />
                </div>

                {/* Phone */}
                <div className="input-group">
                  <Phone className="icon" size={20} />
                  <input 
                    type="tel" 
                    name="phone"
                    placeholder="Phone Number" 
                    value={formData.phone}
                    onChange={handleRegisterInputChange}
                  />
                </div>

                {/* Date of Birth */}
                <div className="input-group">
                  <Calendar className="icon" size={20} />
                  <input 
                    type="date" 
                    name="dob"
                    placeholder="Date of Birth" 
                    value={formData.dob}
                    onChange={handleRegisterInputChange}
                  />
                </div>

                {/* Terms */}
                <div className="options">
                  <label>
                    <input type="checkbox" required />
                    I agree to the Terms & Conditions
                  </label>
                </div>

                {/* Register Button */}
                <button className="login-btn" onClick={handleRegister}>
                  Create Account
                  <ArrowRight size={18} />
                </button>

                {/* Back to Login */}
                <p className="register-text">
                  Already have an account?
                  <span onClick={() => {
                    setShowRegister(false);
                    setShowError("");
                  }}> Login</span>
                </p>
              </>
            ) : (
              // Login Form
              <>
                {/* Email */}
                <div className="input-group">
                  <Mail className="icon" size={20} />
                  <input 
                    type="email" 
                    name="email"
                    placeholder="Email" 
                    value={loginData.email}
                    onChange={handleLoginInputChange}
                  />
                </div>

                {/* Password */}
                <div className="input-group">
                  <Lock className="icon" size={20} />
                  <input 
                    type="password" 
                    name="password"
                    placeholder="Password" 
                    value={loginData.password}
                    onChange={handleLoginInputChange}
                  />
                </div>

                {/* Remember */}
                <div className="options">
                  <label>
                    <input type="checkbox" />
                    Remember Me
                  </label>
                </div>

                {/* Button */}
                <button className="login-btn" onClick={handleLogin}>
                  Login
                  <ArrowRight size={18} />
                </button>

                {/* Register */}
                <p className="register-text">
                  Don't have an account?
                  <span onClick={() => {
                    setShowRegister(true);
                    setShowError("");
                  }}> Register</span>
                </p>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Login;