# 🎓 RHCSA Millionaire - EX200 Exam Prep Game

An interactive CLI-based trivia game to help you prepare for the Red Hat Certified System Administrator (RHCSA) RHEL 10 EX200 exam. Inspired by "Who Wants to Be a Millionaire" and "Slumdog Millionaire", this game features progressive difficulty levels and engaging gameplay mechanics.

## 🎮 Game Features

### Core Mechanics
- **15 Progressive Questions**: Start easy, end hard
- **3 Lives System**: Lose a life for each wrong answer
- **Safe Havens**: Guaranteed score checkpoints at questions 5 and 10
- **Point System**: Earn from 100 to 1,000,000 points
- **3 Lifelines**: Strategic help when you need it

### Lifelines
1. **✂️ 50/50**: Removes two incorrect answers
2. **💡 Hint**: Provides a helpful clue
3. **⏭️ Skip**: Skip the current question (no points earned)

### Scoring System
```
Questions 1-5   (Easy):     100 - 1,000 points
Questions 6-10  (Medium):   2,000 - 32,000 points
Questions 11-15 (Hard):     64,000 - 1,000,000 points
```

### Safe Havens
- **Question 5**: Minimum guaranteed score of 5,000 points
- **Question 10**: Minimum guaranteed score of 50,000 points

## 📚 Topics Covered

The game covers all major RHCSA EX200 exam objectives with **60+ real-world exam questions**:

- **Basic Commands**: Navigation, file operations, finding files
- **User Management**: Creating users, password policies, account management, UID/GID
- **File Permissions**: chmod, chown, ACLs, SGID, special permissions
- **SELinux**: Contexts, booleans, semanage, chcon, restorecon, troubleshooting
- **Networking**: nmcli, network configuration, teaming, static IP configuration
- **Firewall**: firewalld configuration, services, and ports
- **Storage Management**: Partitions, LVM (create, extend, reduce), XFS, ext4, Stratis, VDO, swap
- **System Services**: systemd, systemctl, enabling/disabling services
- **Package Management**: dnf/yum operations, repository configuration
- **Process Management**: ps, top, signals, job control
- **Job Scheduling**: cron, at commands, scheduling patterns
- **Containers**: Podman with systemd integration, user services, persistent containers
- **Boot Process**: GRUB, kernel parameters, boot targets, grubby
- **System Recovery**: Rescue mode, root password reset, SELinux relabeling
- **Logging**: journald persistence, system logs
- **NFS & AutoFS**: Network filesystem mounting, autofs configuration
- **System Tuning**: tuned profiles and performance optimization

## 🚀 Installation & Usage

### Prerequisites
- Python 3.6 or higher
- Linux/Unix terminal (supports ANSI color codes)

### Running the Game

1. **Make the script executable** (if not already):
   ```bash
   chmod +x rhcsa_millionaire.py
   ```

2. **Run the game**:
   ```bash
   ./rhcsa_millionaire.py
   ```
   
   Or:
   ```bash
   python3 rhcsa_millionaire.py
   ```

### Game Controls

During gameplay:
- **A, B, C, D**: Select your answer
- **1**: Use 50/50 lifeline
- **2**: Use Hint lifeline
- **3**: Use Skip lifeline
- **Ctrl+C**: Exit game at any time

## 🎯 How to Play

1. **Start the Game**: Launch the script and press Enter
2. **Read Each Question**: Questions are color-coded by difficulty
   - 🟢 Green = Easy
   - 🟡 Yellow = Medium
   - 🔴 Red = Hard
3. **Choose Your Answer**: Type A, B, C, or D
4. **Use Lifelines Strategically**: Each can only be used once
5. **Track Your Progress**: Monitor your score, lives, and question number
6. **Review Your Performance**: At the end, see topic-by-topic breakdown

## 📊 Post-Game Statistics

After completing the game, you'll see:
- **Final Score**: Total points earned
- **Questions Answered**: How many you completed
- **Accuracy Percentage**: Overall correctness rate
- **Topic Performance**: Breakdown by subject area with visual bars
- **Answer Review**: Optional detailed review of all questions

## 💡 Study Tips

1. **Play Multiple Times**: Questions are randomized each game
2. **Review Wrong Answers**: Read the explanations carefully
3. **Focus on Weak Topics**: Use the topic performance stats to identify areas needing study
4. **Practice Commands**: Try the commands mentioned in questions on a real RHEL system
5. **Use Lifelines Wisely**: Save them for harder questions

## 🎓 Exam Preparation Strategy

### Before the Exam
- Play the game multiple times until you consistently score high
- Set up a RHEL 10 practice environment
- Practice hands-on labs for topics where you score poorly
- Review Red Hat documentation for weak areas

### During the Game
- Read questions carefully - some have multiple correct methods
- Pay attention to explanations even when you answer correctly
- Note topics where you struggle for focused study

### Difficulty Progression
- **Easy Questions (1-5)**: Basic commands and concepts
- **Medium Questions (6-10)**: Practical administration tasks
- **Hard Questions (11-15)**: Advanced scenarios and edge cases

## 🔧 Technical Details

### Question Database
- **17 Easy Questions**: Fundamental concepts and basic commands
- **20 Medium Questions**: Intermediate administration and practical tasks
- **20 Hard Questions**: Advanced topics, complex multi-step scenarios
- **Random Selection**: 5 from each difficulty level per game (15 total per session)
- **Questions sourced from**: Real RHCSA exam guides and practice scenarios

### Color Coding
The game uses ANSI color codes for enhanced visual experience:
- 🔵 Cyan: Headers and information
- 🟢 Green: Correct answers and success
- 🟡 Yellow: Warnings and hints
- 🔴 Red: Wrong answers and errors
- ⚪ Bold: Important text and questions

## 📝 Example Gameplay

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🎓  RHCSA MILLIONAIRE  🎓                       ║
║                                                           ║
║     Red Hat Certified System Administrator EX200         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════
  Question: 1/15  |  Score: 0  |  Lives: ❤️ ❤️ ❤️ 
  Lifelines: ✂️  50/50 ✓ | 💡 Hint ✓ | ⏭️  Skip ✓
═══════════════════════════════════════════════════════════

  [EASY]
  Worth: 100 points

  What command is used to display the current working directory?

    A: ls
    B: pwd
    C: cd
    D: dir

  Your answer (A/B/C/D) or lifeline (1=50/50, 2=Hint, 3=Skip): 
```

## 🏆 Scoring Milestones

- **5,000+ points**: RHCSA Beginner
- **50,000+ points**: RHCSA Intermediate
- **250,000+ points**: RHCSA Advanced
- **1,000,000 points**: RHCSA MASTER! 🎉

## 🐛 Troubleshooting

### Colors Not Displaying
If colors don't display properly:
- Ensure your terminal supports ANSI color codes
- Try a different terminal emulator (e.g., GNOME Terminal, Konsole)

### Python Version Issues
If you encounter errors:
```bash
python3 --version  # Check your Python version
```
Ensure you have Python 3.6 or higher.

## 📖 Additional Resources

### Official Red Hat Resources
- [RHCSA Exam Objectives (EX200)](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam)
- [Red Hat Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/10)

### Practice Environments
- Red Hat Developer Subscription (free)
- VirtualBox/KVM with RHEL 10
- Cloud providers with RHEL instances

## 🤝 Contributing

Want to add more questions or improve the game? The question database is in the `load_questions()` method. Each question includes:
- Question text
- Four options (A, B, C, D)
- Correct answer index (0-3)
- Difficulty level
- Topic category
- Hint text
- Detailed explanation

## 📄 License

This is an educational tool created for RHCSA exam preparation. Use it to supplement your studies and hands-on practice.

## ⚠️ Disclaimer

This game is a study aid and does not guarantee passing the RHCSA exam. Hands-on practice with real RHEL systems is essential for exam success. The questions are based on common RHCSA topics but may not reflect the exact exam content.

---

**Good luck on your RHCSA journey! 🎓🚀**

*Remember: The best way to learn Linux is by doing. Use this game to identify knowledge gaps, then practice those skills on a real system!*