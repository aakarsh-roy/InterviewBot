# 🤖 Advanced Interview Preparation Bot

An AI-powered interview preparation platform that helps you practice technical interviews with intelligent question generation, real-time hints, and detailed feedback.

## ✨ Features

### 🎯 Core Features
- **Multi-Question Type Support**
  - Technical Knowledge Questions
  - Coding Challenges
  - Behavioral Questions
  - System Design Questions

- **Adaptive Difficulty**
  - Easy, Medium, Hard levels
  - Automatic difficulty adjustment based on performance
  - Smart suggestions for next difficulty level

- **Comprehensive Tech Stack Coverage**
  - Python, JavaScript, Java, C++
  - React, Node.js
  - Web Development, Data Science
  - Machine Learning, DevOps
  - System Design

### 🧠 AI-Powered Features
- **Intelligent Question Generation**
  - Context-aware questions
  - Avoids repetition in the same session
  - Clean, formatted questions without markdown

- **Smart Hints System**
  - Get hints when stuck
  - Context-aware based on your current answer
  - Doesn't give away the complete solution

- **Detailed Feedback**
  - Structured scoring (0-10)
  - Strengths analysis
  - Areas for improvement
  - Technical suggestions with examples
  - Sample answer approach
  - Next steps for learning

### 📊 Session Tracking
- **Progress Monitoring**
  - Track questions answered
  - Average score calculation
  - Session statistics
  - Performance trends

- **Real-time Metrics**
  - Time tracking per question
  - Score per question
  - Overall session performance

### 🎨 User Experience
- **Modern UI/UX**
  - Beautiful gradient design
  - Smooth animations
  - Responsive layout for all devices
  - Intuitive navigation

- **Interactive Features**
  - Auto-save answers (localStorage)
  - Character counter
  - Timer display
  - Speech-to-text support (browser dependent)
  - Copy question to clipboard
  - Quick tips on demand

### 🔄 Session Management
- **Continuous Learning**
  - Next question generation
  - Session persistence
  - Progress tracking across questions
  - Reset session option

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/InterviewBot.git
   cd InterviewBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage Guide

### Starting an Interview

1. **Select Your Preferences**
   - Choose a tech stack (e.g., Python, JavaScript)
   - Select difficulty level (Easy, Medium, Hard)
   - Pick question type (Technical, Coding, Behavioral, System Design)

2. **Get Questions**
   - Click "Start Interview" for selected preferences
   - Or click "Random" for a surprise question

3. **Answer the Question**
   - Type your answer in the text area
   - Use "Need Hint" if you're stuck
   - Click "Get Feedback" when ready

### During the Interview

- **Timer**: Automatically tracks time spent on each question
- **Character Counter**: Shows answer length
- **Auto-save**: Your answer is saved as you type
- **Hints**: Click "Need Hint" for guidance without spoilers

### After Answering

- **View Detailed Feedback**: See your score, strengths, and areas to improve
- **Check Statistics**: View session progress and average score
- **Continue Learning**: Click "Next Question" for adaptive difficulty
- **Share Results**: Share your performance on social media

### Session Management

- **Reset Session**: Clear all progress and start fresh
- **Continue Session**: Keep building on your current session
- **Track Progress**: Monitor improvement across multiple questions

## 🎯 Question Types Explained

### Technical Knowledge
- Focuses on theoretical concepts
- Tests understanding of fundamentals
- Covers best practices and patterns

### Coding Challenge
- Algorithmic problem-solving
- Implementation tasks
- Code optimization challenges

### Behavioral
- Real-world scenarios
- Teamwork and communication
- Problem-solving approach

### System Design
- Architecture questions
- Scalability challenges
- Design pattern discussions

## 📊 Scoring System

Questions are scored on a scale of 0-10:

- **0-3**: Needs significant improvement
- **4-6**: Satisfactory with room for growth
- **7-8**: Good performance
- **9-10**: Excellent, ready for harder challenges

The system automatically suggests difficulty adjustments:
- Score ≥8: Try harder difficulty
- Score ≤4: Try easier difficulty

## 🛠️ Technical Architecture

### Backend (Flask)
- **Routes**:
  - `/` - Main interface
  - `/ask_question` - Question generation
  - `/give_feedback` - Answer evaluation
  - `/api/get_hint` - Hint generation
  - `/api/random_question` - Random question
  - `/api/quick_tip` - Interview tips
  - `/api/session_stats` - Session statistics
  - `/reset_session` - Clear session
  - `/next_question` - Continue interview

### Frontend
- **HTML/CSS**: Modern responsive design
- **JavaScript**: Interactive features, AJAX calls
- **LocalStorage**: Auto-save functionality

### AI Integration
- **Google Gemini API**: Question generation, hints, feedback
- **Smart Prompting**: Context-aware, clean output
- **Text Processing**: Format cleaning, structured parsing

## 🔐 Security & Privacy

- Sessions are stored in-memory (not persistent)
- No personal data collection
- API keys secured via environment variables
- Session data cleared on browser close

## 🎨 Customization

### Adding New Tech Stacks
Edit `app.py` and add to the tech_stacks list:
```python
tech_stacks = ["Python", "YourNewStack", ...]
```

### Modifying Difficulty Levels
Adjust prompts in the `generate_question` function.

### Changing UI Theme
Edit `static/style.css` gradient colors and styling.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for powering the intelligent features
- Flask framework for the backend
- All contributors and users of this project

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**Happy Interviewing! 🚀**
