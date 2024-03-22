import React, { useState } from 'react';
import { Input, Button, Typography, Card, Divider, Upload, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

const ChatPage = () => {
  const [inputValue, setInputValue] = useState('');
  const [showLoader, setShowLoader] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'system', content: '1. Click on Activate Proton GPT button' },
    { role: 'system', content: '2. Upload some files' },
    { role: 'system', content: '3. Ask Questions' },
  ]);
//   const [chatbotAnswer, setChatbotAnswer] = useState([{ role: 'system', content: 'chatbot predicts...' }]);
  const [file, setFile] = useState(null);

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    try {
        setShowLoader(true);
      await axios.post('http://localhost:8000/chatbot/upload_file', formData);
      setShowLoader(false);
      message.success('File uploaded successfully.');
    } catch (error) {
      message.error('File upload failed.');
    }
  };

  const handleActivate = async () => {
        try {
          setShowLoader(true);
          await axios.get('http://localhost:8000/chatbot/initialize');
          const new_messages = [
            { role: 'user', content: "Activate Proton GPT" },
            { role: 'system', content: "Activated. Ready to use now." },
            { role: 'system', content: "Kindly upload a file to get started" }
          ]
          setMessages([...messages, ...new_messages]);
          message.success('Proton GPT activated.');
          setShowLoader(false);
        } catch (error) {
          message.error('Failed to activate Proton GPT.');
        }
      };

  const handleSubmit = async () => {
    try {
        const new_messages = [
            { role: 'user', content: inputValue },
          ]
        setInputValue('');  
        setMessages([...messages, ...new_messages]);
        setShowLoader(true);
        const res = await axios.post('http://localhost:8000/chatbot/predict', {
            question: inputValue
            }
        );
        setShowLoader(false);
        const answer = res.data.result
        const updated_response = [
            { role: 'system', content: answer },
        ]
        setMessages([...messages, ...new_messages, ...updated_response]);
    } catch (error) {
      console.error(error);
    }
  };

  const uploadProps = {
    name: 'file',
    beforeUpload: (file) => {
      const allowedExt = ['.pdf', '.csv', '.txt', '.docx'];
      const { type, name } = file;
      const ext = name.substring(name.lastIndexOf('.'));
      if (!allowedExt.includes(ext)) {
        message.error(`Only ${allowedExt.join(', ')} files are supported.`);
      }
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('File must be smaller than 10MB.');
      }
    //   return allowedExt.includes(ext) && isLt10M;
    //   return false;
      setFile(file);
      return false;
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
    <div style={{ marginLeft: 250, marginRight: 250}}>
      <Card className="chat-page">
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <Title level={2} className="welcome-text">Welcome to Proton GPT</Title>
        </div>

        
        <div style={{display: 'flex', justifyContent: 'center', marginBottom: 20}}>   
        <Button className="activate-button" type="primary" size='large' onClick={handleActivate}>
            Activate Proton GPT
        </Button>
        </div>
        <div style={{display: 'flex', marginTop: '10px', justifyContent: 'center'}}>
        <Upload {...uploadProps}>
            <Button style={{marginRight: 10}} icon={<PlusOutlined  />}>Browse File</Button>
          </Upload>
          <Button style={{backgroundColor: 'green'}} className="upload-button" onClick={handleFileUpload} type="primary" icon={<UploadOutlined  />}>Upload File</Button>
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
            {/* <TypingLoader show={showLoader} /> */}
            <div className="dot-flashing" style={{ marginLeft: 20, display: showLoader ? 'block' : 'none' }}>
            </div>
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
          left: 240,
          bottom: 0,
          right: 240,
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
                icon={<PlusOutlined />}
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




