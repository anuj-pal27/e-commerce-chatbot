import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../../services/api';
import ChatMessage from './ChatMessage';

const ChatInterface = ({ user, setUser }) => {
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sendingMessage, setSendingMessage] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load chat sessions on component mount
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const response = await chatAPI.getSessions();
      setSessions(response.data);
      
      // If there are existing sessions, load the most recent one
      if (response.data.length > 0) {
        loadSession(response.data[0]);
      } else {
        // Create a new session if none exist
        createNewSession();
      }
    } catch (error) {
      console.error('Error loading sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const createNewSession = async () => {
    try {
      setLoading(true);
      const response = await chatAPI.createSession();
      const newSession = response.data;
      setSessions(prev => [newSession, ...prev]);
      loadSession(newSession);
    } catch (error) {
      console.error('Error creating session:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSession = async (session) => {
    try {
      setCurrentSession(session);
      const response = await chatAPI.getMessages(session.session_id);
      setMessages(response.data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const resetCurrentSession = async () => {
    if (!currentSession) return;
    
    try {
      setLoading(true);
      await chatAPI.resetSession(currentSession.session_id);
      loadSession(currentSession);
    } catch (error) {
      console.error('Error resetting session:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteSession = async (sessionId) => {
    try {
      await chatAPI.deleteSession(sessionId);
      setSessions(prev => prev.filter(s => s.session_id !== sessionId));
      
      if (currentSession?.session_id === sessionId) {
        const remainingSessions = sessions.filter(s => s.session_id !== sessionId);
        if (remainingSessions.length > 0) {
          loadSession(remainingSessions[0]);
        } else {
          createNewSession();
        }
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !currentSession || sendingMessage) return;

    const messageContent = newMessage.trim();
    setNewMessage('');
    setSendingMessage(true);

    try {
      const response = await chatAPI.sendMessage(currentSession.session_id, messageContent);
      
      // Add both user and bot messages to the state
      setMessages(prev => [...prev, response.data.user_message, response.data.bot_message]);
      
      // Update session in the list
      setSessions(prev => prev.map(session => 
        session.session_id === currentSession.session_id 
          ? { ...session, updated_at: new Date().toISOString() }
          : session
      ));
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setSendingMessage(false);
    }
  };

  const getSuggestedQueries = () => [
    "Show me electronics",
    "I need a laptop",
    "What books do you have?",
    "Show me furniture under $200",
    "I'm looking for toys",
    "What are your latest textiles?"
  ];

  const handleSuggestedQuery = (query) => {
    setNewMessage(query);
  };

  if (loading && !currentSession) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="h-screen flex bg-gray-100">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-80' : 'w-16'} lg:w-80 bg-white border-r border-gray-200 transition-all duration-300 flex-shrink-0`}>
        <div className="p-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <h2 className={`font-semibold text-gray-900 ${sidebarOpen ? 'block' : 'hidden'} lg:block`}>
              Chat Sessions
            </h2>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden p-2 rounded-md hover:bg-gray-100"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>

          {/* New Chat Button */}
          <button
            onClick={createNewSession}
            className={`w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 mb-4 ${sidebarOpen ? 'block' : 'hidden'} lg:block`}
          >
            + New Chat
          </button>

          {/* Session List */}
          <div className={`space-y-2 ${sidebarOpen ? 'block' : 'hidden'} lg:block`}>
            {sessions.map((session) => (
              <div
                key={session.session_id}
                className={`p-3 rounded-md cursor-pointer ${
                  currentSession?.session_id === session.session_id
                    ? 'bg-blue-100 border border-blue-300'
                    : 'hover:bg-gray-100'
                }`}
                onClick={() => loadSession(session)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-sm text-gray-900">
                      Chat {session.session_id.substring(0, 8)}...
                    </div>
                    <div className="text-xs text-gray-500">
                      {new Date(session.updated_at).toLocaleDateString()}
                    </div>
                    <div className="text-xs text-gray-400">
                      {session.message_count} messages
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteSession(session.session_id);
                    }}
                    className="text-red-500 hover:text-red-700 p-1 rounded"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden mr-3 p-2 rounded-md hover:bg-gray-100"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <h1 className="text-xl font-semibold text-gray-900">Shopping Assistant</h1>
            <span className="ml-2 text-sm text-green-500">● Online</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={resetCurrentSession}
              className="bg-gray-100 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-200"
            >
              Reset Chat
            </button>
            <span className="text-sm text-gray-600">
              Welcome, {user?.first_name}!
            </span>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && !loading ? (
            <div className="text-center py-8">
              <div className="text-gray-500 mb-4">
                <h3 className="text-lg font-medium">Welcome to our Shopping Assistant!</h3>
                <p className="text-sm mt-2">Ask me about products, categories, or anything you're looking for.</p>
              </div>
              
              {/* Suggested Queries */}
              <div className="mt-6">
                <p className="text-sm text-gray-600 mb-3">Try asking:</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-md mx-auto">
                  {getSuggestedQueries().map((query, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestedQuery(query)}
                      className="text-left p-2 bg-gray-100 rounded hover:bg-gray-200 text-sm"
                    >
                      "{query}"
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                isUser={message.message_type === 'user'}
              />
            ))
          )}
          
          {sendingMessage && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg p-3 max-w-xs">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input */}
        <div className="bg-white border-t border-gray-200 p-4">
          <form onSubmit={sendMessage} className="flex space-x-3">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Ask about products, categories, or anything you need..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={sendingMessage}
            />
            <button
              type="submit"
              disabled={!newMessage.trim() || sendingMessage}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 