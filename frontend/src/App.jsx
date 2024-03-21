import React, { useState } from 'react';
import { Input, Button, Typography, Card, Divider, Upload, message } from 'antd';
import { ArrowUpOutlined, PlusOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

const ChatPage = () => {
  const [inputValue, setInputValue] = useState('');
  const [showLoader, setShowLoader] = useState(true);
  const [messages, setMessages] = useState([
    { role: 'system', content: '1. Click on Activate Proton GPT button' },
    { role: 'system', content: '2. Upload some files' },
    { role: 'system', content: '3. Ask Questions' },
  ]);
  const [file, setFile] = useState(null);

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post('http://localhost:8000/chatbot/upload-file', formData);
      message.success('File uploaded successfully.');
    } catch (error) {
      message.error('File upload failed.');
    }
  };

  const handleActivate = async () => {
    const new_messages = [
      { role: 'user', content: "Activate Proton GPT" },
      { role: 'system', content: "Activating..." }
    ]
    setMessages([...messages, ...new_messages]);
    try {
      const response = await axios.get('http://localhost:8000/chatbot/initialize');
      const final_message = [{ role: 'user', content: "Activate Proton GPT" },
      { role: 'system', content: "Activating..." },
      { role: 'system', content: "ProtonGPT Activated!" }]
      setMessages([...messages, final_message]);
      message.success('Proton GPT activated.');
    } catch (error) {
      const final_message = { role: 'system', content: "Failed to activate Proton GPT." }
      setMessages([...messages, final_message]);
      message.error('Failed to activate Proton GPT.');
    }
  };

  const handleSubmit = () => {
    setShowLoader(false);
    const newMessage = { role: 'user', content: inputValue };
    setMessages([...messages, newMessage]);
    setInputValue('');
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    beforeUpload: (file) => {
      const allowedExt = ['.pdf', '.csv', '.txt', '.docx'];
      const { type, name } = file;
      const ext = name.substring(name.lastIndexOf('.'));
      if (!allowedExt.includes(ext)) {
        message.error(`Only ${allowedExt.join(', ')} files are supported.`);
      }
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        message.error('File must be smaller than 2MB.');
      }
      return allowedExt.includes(ext) && isLt2M;
    },
    onChange: (info) => {
      const { status } = info.file;
      if (status === 'done') {
        setFile(info.file.originFileObj);
      }
    },
  };

  
  const text_style = (message)  => {
    if (message.role == "user"){
      return { flex: 1, textAlign: 'right' }
    }
    return { flex: 1, textAlign: 'left' }
  }

  const TypingLoader = ({show}) => {
    
    // if show
    return (
      <div className="dot-flashing" style={{marginLeft: 20}}>
      </div>
    );
  };


  return (
    <div style={{ marginLeft: 150, marginRight: 150}}>
      <Card className="chat-page">
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <Title level={2} className="welcome-text">Welcome to Proton GPT</Title>
        </div>
        {/* <div style={{display: 'flex', justifyContent: 'center', marginTop: 20}}>
          <Button className="activate-button" type="primary" onClick={handleActivate}>
            Activate Proton GPT
          </Button>
        </div> */}

        
        <div style={{display: 'flex', justifyContent: 'space-between'}}>
        
          <Upload {...uploadProps}>
            <Button style={{marginRight: 10}} icon={<PlusOutlined />}>Browse File</Button>
            <Button className="upload-button" onClick={handleFileUpload} type="primary">Upload File</Button>
          </Upload>
          
          <Button className="activate-button" type="primary" onClick={handleActivate}>
            Activate Proton GPT
          </Button>
        </div>
        
        <Divider />
        <div style={{ display: 'flex', alignItems: 'center', marginTop: 20 }}>
          <Title level={4} className="message-text" style={{ flex: 1, textAlign: 'left' , }}>Proton GPT</Title>
        </div>

        <div style={{
          height: 300, 
          overflowY: 'scroll', 
          paddingRight: 20, 
          marginTop: 20,
          marginBottom: 50
        }}>
          {messages.map((message, index) => (
            <div key={index} className='message' style={{ display: 'flex', alignItems: 'center'}}>
              <Text level={4} className={"message-text"} style={text_style(message)}>{message.content}</Text>
              {/* <TypingLoader show={message.role === 'system' ? true : false} /> */}
            </div>
            
          ))}

          <div className='message' style={{ display: 'flex', alignItems: 'center', marginTop: 20}}>
            {/* <Text level={4} className={"message-text"} style={{ flex: 1, textAlign: 'left' }}>abcd</Text> */}
            <TypingLoader show={showLoader} />
            {/* <div className="dot-flashing" style={{ marginLeft: 20, display: true ? 'block' : 'none' }}>
            </div> */}
          </div>
        </div>
 

        {/* {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`} style={{display: 'flex', alignItems: 'center'}}>
            <Text className="message-text" style={{textAlign: 'right'}}>{message.content}</Text>
          </div>
        ))} */}

        <footer style={{
          display: 'flex',
          justifyContent: 'center',
          padding: 20,
          paddingTop: 5,
          position: 'fixed',
          left: 135,
          right: 135,
          bottom: 0,
          backgroundColor: 'white',
        }}>
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onPressEnter={handleSubmit}
            placeholder="Enter your question"
            suffix={
              <Button
                className="chat-submit-button"
                type="primary"
                onClick={handleSubmit}
                icon={<ArrowUpOutlined />}
              >
                Submit
              </Button>
            }
          />
        </footer>

      </Card>
    </div>
  );
};

export default ChatPage;




