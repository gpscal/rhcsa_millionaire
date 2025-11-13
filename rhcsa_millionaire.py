#!/usr/bin/env python3
"""
RHCSA Millionaire - CLI-based RHEL 10 EX200 Exam Preparation Game
A Slumdog Millionaire-style trivia game for RHCSA certification prep
"""

import os
import sys
import time
import random
from typing import List, Dict, Tuple

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_colored(text: str, color: str = Colors.END, end='\n'):
    """Print colored text"""
    print(f"{color}{text}{Colors.END}", end=end)

def print_banner():
    """Display the game banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🎓  RHCSA MILLIONAIRE  🎓                       ║
    ║                                                           ║
    ║     Red Hat Certified System Administrator EX200         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN + Colors.BOLD)

def print_separator():
    """Print a separator line"""
    print_colored("═" * 63, Colors.BLUE)

def animate_text(text: str, delay: float = 0.03):
    """Animate text output character by character"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class Question:
    """Represents a single trivia question"""
    def __init__(self, question: str, options: List[str], correct: int, 
                 difficulty: str, topic: str, hint: str, explanation: str):
        self.question = question
        self.options = options
        self.correct = correct
        self.difficulty = difficulty
        self.topic = topic
        self.hint = hint
        self.explanation = explanation

class Game:
    """Main game class"""
    
    # Point values for each question level
    POINT_VALUES = [
        100, 200, 300, 500, 1000,           # Questions 1-5 (Easy)
        2000, 4000, 8000, 16000, 32000,     # Questions 6-10 (Medium)
        64000, 125000, 250000, 500000, 1000000  # Questions 11-15 (Hard)
    ]
    
    SAFE_HAVENS = [5, 10]  # Question numbers where score is guaranteed
    
    def __init__(self):
        self.score = 0
        self.current_question = 0
        self.lives = 3
        self.lifelines = {'5050': True, 'hint': True, 'skip': True}
        self.questions_pool = self.load_questions()
        self.selected_questions = []
        self.answers_history = []
        self.topic_stats = {}
        
    def load_questions(self) -> Dict[str, List[Question]]:
        """Load all questions organized by difficulty"""
        questions = {
            'easy': [
                Question(
                    "What command is used to display the current working directory?",
                    ["A: ls", "B: pwd", "C: cd", "D: dir"],
                    1, "easy", "Basic Commands",
                    "This command 'prints' the 'working directory'",
                    "pwd (print working directory) displays the full path of the current directory."
                ),
                Question(
                    "Which file contains user account information in Linux?",
                    ["A: /etc/shadow", "B: /etc/group", "C: /etc/passwd", "D: /etc/users"],
                    2, "easy", "User Management",
                    "This file has 'passwd' in its name",
                    "/etc/passwd contains user account information including username, UID, GID, home directory, and shell."
                ),
                Question(
                    "What is the default permission for newly created files (without umask)?",
                    ["A: 777", "B: 755", "C: 666", "D: 644"],
                    2, "easy", "File Permissions",
                    "Files don't get execute permission by default",
                    "The default permission for files is 666 (rw-rw-rw-), which is then modified by umask."
                ),
                Question(
                    "Which command is used to change file ownership?",
                    ["A: chmod", "B: chown", "C: chgrp", "D: chattr"],
                    1, "easy", "File Permissions",
                    "The command name includes 'own'",
                    "chown (change owner) is used to change the user and/or group ownership of files."
                ),
                Question(
                    "What does the 'systemctl status' command do?",
                    ["A: Shows system time", "B: Displays service status", "C: Shows disk status", "D: Displays CPU status"],
                    1, "easy", "System Services",
                    "systemctl manages system services",
                    "systemctl status displays the current status of a systemd service or unit."
                ),
                Question(
                    "Which directory contains system log files?",
                    ["A: /var/log", "B: /etc/log", "C: /usr/log", "D: /tmp/log"],
                    0, "easy", "Logging",
                    "Variable data like logs go in /var",
                    "/var/log is the standard directory for system log files in Linux."
                ),
                Question(
                    "What command displays running processes?",
                    ["A: ls", "B: ps", "C: top", "D: Both B and C"],
                    3, "easy", "Process Management",
                    "Multiple commands can show processes",
                    "Both ps and top display running processes, with top providing real-time updates."
                ),
                Question(
                    "Which package manager is used in RHEL 10?",
                    ["A: apt", "B: yum", "C: dnf", "D: pacman"],
                    2, "easy", "Package Management",
                    "RHEL 8+ uses the 'dandified' version",
                    "dnf (Dandified YUM) is the default package manager in RHEL 8 and later versions."
                ),
            ],
            'medium': [
                Question(
                    "What is the correct syntax to create a logical volume named 'lv_data' of size 5GB in volume group 'vg_main'?",
                    ["A: lvcreate -L 5G -n lv_data vg_main", "B: lvcreate -n lv_data -L 5G vg_main", 
                     "C: lvmcreate -L 5GB lv_data vg_main", "D: Both A and B"],
                    3, "medium", "LVM",
                    "Both -L and -n flag orders work",
                    "lvcreate accepts flags in any order. Both 'lvcreate -L 5G -n lv_data vg_main' and 'lvcreate -n lv_data -L 5G vg_main' are correct."
                ),
                Question(
                    "Which SELinux boolean allows httpd to connect to network databases?",
                    ["A: httpd_can_network_connect", "B: httpd_can_network_connect_db", 
                     "C: httpd_enable_network_db", "D: httpd_network_db_access"],
                    1, "medium", "SELinux",
                    "The boolean name is very descriptive and includes 'db'",
                    "httpd_can_network_connect_db is the SELinux boolean that allows Apache to connect to remote databases."
                ),
                Question(
                    "What command sets a static IP address using nmcli?",
                    ["A: nmcli con mod eth0 ipv4.addresses 192.168.1.10/24", 
                     "B: nmcli dev set eth0 ip 192.168.1.10/24",
                     "C: nmcli connection modify eth0 ip.address 192.168.1.10/24", 
                     "D: nmcli set eth0 ipv4 192.168.1.10/24"],
                    0, "medium", "Networking",
                    "Use 'con mod' with ipv4.addresses",
                    "nmcli con mod <connection> ipv4.addresses <IP/prefix> is the correct syntax for setting a static IP."
                ),
                Question(
                    "Which file should you edit to make a filesystem mount automatically at boot?",
                    ["A: /etc/mtab", "B: /etc/fstab", "C: /proc/mounts", "D: /etc/auto.mount"],
                    1, "medium", "Storage Management",
                    "The 'fs' stands for filesystem",
                    "/etc/fstab (filesystem table) contains information about filesystems to mount at boot time."
                ),
                Question(
                    "What is the correct command to add a firewall rule allowing HTTP traffic?",
                    ["A: firewall-cmd --add-service=http --permanent", 
                     "B: iptables -A INPUT -p tcp --dport 80 -j ACCEPT",
                     "C: firewall-cmd --permanent --add-port=80/tcp", 
                     "D: Both A and C"],
                    3, "medium", "Firewall",
                    "Multiple methods work with firewalld",
                    "Both adding the http service and opening port 80/tcp are valid methods with firewall-cmd."
                ),
                Question(
                    "How do you set a password to expire in 90 days for user 'john'?",
                    ["A: chage -M 90 john", "B: passwd -e 90 john", 
                     "C: usermod --expiredate 90 john", "D: passwd --maxdays 90 john"],
                    0, "medium", "User Management",
                    "chage manages password aging, -M is for maximum days",
                    "chage -M 90 john sets the maximum number of days between password changes to 90."
                ),
                Question(
                    "What command creates a compressed tar archive?",
                    ["A: tar -czf archive.tar.gz files/", "B: tar -xzf archive.tar.gz", 
                     "C: gzip -c files/ > archive.tar.gz", "D: compress -z files/ archive.tar.gz"],
                    0, "medium", "File Management",
                    "c=create, z=gzip, f=file",
                    "tar -czf creates a gzip-compressed tar archive. c=create, z=gzip compression, f=filename."
                ),
                Question(
                    "Which command shows all currently loaded kernel modules?",
                    ["A: modprobe -l", "B: lsmod", "C: insmod --list", "D: kmod list"],
                    1, "medium", "Kernel Management",
                    "ls usually means 'list'",
                    "lsmod lists all currently loaded kernel modules by reading /proc/modules."
                ),
                Question(
                    "What is the correct ACL command to give user 'bob' read and write access to file.txt?",
                    ["A: setfacl -m u:bob:rw file.txt", "B: setfacl -m user:bob:rw file.txt",
                     "C: setfacl --modify u:bob:rw file.txt", "D: All of the above"],
                    3, "medium", "ACLs",
                    "setfacl accepts multiple syntax formats",
                    "All three syntaxes are valid for setfacl. -m and --modify are equivalent, and u: and user: are interchangeable."
                ),
                Question(
                    "How do you schedule a one-time job to run at 2:30 AM tomorrow?",
                    ["A: at 02:30 tomorrow", "B: cron 02:30 +1day", 
                     "C: schedule --time 02:30 --date tomorrow", "D: systemd-run --on-calendar tomorrow 02:30"],
                    0, "medium", "Job Scheduling",
                    "The 'at' command is for one-time jobs",
                    "The 'at' command schedules one-time jobs. 'at 02:30 tomorrow' schedules a job for 2:30 AM the next day."
                ),
            ],
            'hard': [
                Question(
                    "What is the correct procedure to extend an XFS filesystem on a logical volume?",
                    ["A: lvextend -L +5G /dev/vg/lv && xfs_growfs /mount/point", 
                     "B: lvextend -L +5G /dev/vg/lv && resize2fs /dev/vg/lv",
                     "C: lvresize -L +5G /dev/vg/lv && xfs_resize /dev/vg/lv", 
                     "D: vgextend -L +5G /dev/vg/lv && xfs_growfs /mount/point"],
                    0, "hard", "LVM & Filesystems",
                    "XFS uses xfs_growfs, not resize2fs",
                    "For XFS, you must first extend the LV with lvextend, then grow the filesystem with xfs_growfs using the mount point."
                ),
                Question(
                    "Which command correctly configures a Podman container to start automatically at boot as a systemd service?",
                    ["A: podman generate systemd --name mycontainer --files --new", 
                     "B: systemctl enable podman-mycontainer.service",
                     "C: podman create --restart=always mycontainer", 
                     "D: podman systemd-enable mycontainer"],
                    0, "hard", "Containers",
                    "Podman can generate systemd unit files",
                    "podman generate systemd creates systemd unit files for containers. The --new flag recreates the container on start."
                ),
                Question(
                    "What is the correct SELinux context type for files in /var/www/html/?",
                    ["A: httpd_sys_content_t", "B: httpd_sys_script_exec_t", 
                     "C: public_content_t", "D: user_home_t"],
                    0, "hard", "SELinux",
                    "httpd_sys_content_t is for web content",
                    "httpd_sys_content_t is the correct SELinux type for static web content in Apache's document root."
                ),
                Question(
                    "How do you configure a network team interface with activebackup runner using nmcli?",
                    ["A: nmcli con add type team con-name team0 ifname team0 config '{\"runner\": {\"name\": \"activebackup\"}}'",
                     "B: nmcli dev team add team0 mode activebackup",
                     "C: nmcli connection team create team0 --runner activebackup",
                     "D: ip link add team0 type team mode activebackup"],
                    0, "hard", "Advanced Networking",
                    "nmcli uses JSON config for team interfaces",
                    "Network teaming in nmcli requires a JSON configuration string specifying the runner type."
                ),
                Question(
                    "What is the correct command to reset the root password from rescue mode?",
                    ["A: mount -o remount,rw /sysroot && chroot /sysroot && passwd root && touch /.autorelabel",
                     "B: chroot /sysroot && passwd root && reboot",
                     "C: mount /dev/sda1 /mnt && chroot /mnt && passwd",
                     "D: passwd --root=/sysroot root"],
                    0, "hard", "System Recovery",
                    "Must remount rw, chroot, change password, and trigger SELinux relabel",
                    "The complete procedure requires remounting /sysroot as read-write, chrooting, changing password, and creating /.autorelabel for SELinux."
                ),
                Question(
                    "Which command creates a stratis pool named 'pool1' using /dev/sdb and /dev/sdc?",
                    ["A: stratis pool create pool1 /dev/sdb /dev/sdc", 
                     "B: stratis create pool pool1 /dev/sdb /dev/sdc",
                     "C: stratis-pool --create pool1 --devices /dev/sdb,/dev/sdc",
                     "D: stratisctl pool add pool1 /dev/sdb /dev/sdc"],
                    0, "hard", "Stratis Storage",
                    "The syntax is 'stratis pool create'",
                    "stratis pool create <pool_name> <device1> <device2> is the correct syntax for creating a Stratis pool."
                ),
                Question(
                    "How do you configure persistent kernel parameters?",
                    ["A: Edit /etc/default/grub, add to GRUB_CMDLINE_LINUX, run grub2-mkconfig -o /boot/grub2/grub.cfg",
                     "B: Edit /boot/grub2/grub.cfg directly",
                     "C: Use grubby --update-kernel=ALL --args='parameter'",
                     "D: Both A and C"],
                    3, "hard", "Boot Process",
                    "Both methods work for persistent kernel parameters",
                    "Both editing /etc/default/grub and using grubby are valid methods for setting persistent kernel parameters."
                ),
                Question(
                    "What is the correct syntax for a cron job that runs every 15 minutes during business hours (9 AM - 5 PM) on weekdays?",
                    ["A: */15 9-17 * * 1-5", "B: 0,15,30,45 9-17 * * 1-5",
                     "C: */15 9-17 * * MON-FRI", "D: All of the above"],
                    3, "hard", "Advanced Scheduling",
                    "Multiple valid cron syntaxes exist",
                    "All three syntaxes are valid. */15 means every 15 minutes, 9-17 is 9 AM to 5 PM, and 1-5 or MON-FRI represents weekdays."
                ),
                Question(
                    "Which command correctly configures a VDO volume with 10:1 logical to physical ratio?",
                    ["A: vdo create --name=vdo1 --device=/dev/sdb --vdoLogicalSize=100G --vdoPhysicalSize=10G",
                     "B: vdo create --name=vdo1 --device=/dev/sdb --vdoLogicalSize=10G",
                     "C: lvcreate --type vdo -L 10G -V 100G -n vdo1 vg_name",
                     "D: Both B and C"],
                    3, "hard", "VDO Storage",
                    "VDO can be created standalone or as LVM type",
                    "Both standalone VDO and LVM-VDO are valid. With LVM: -L is physical size, -V is virtual/logical size."
                ),
                Question(
                    "How do you configure a system to automatically mount an NFS share at boot with specific options?",
                    ["A: Add to /etc/fstab: server:/share /mnt/nfs nfs defaults,_netdev 0 0",
                     "B: Add to /etc/fstab: server:/share /mnt/nfs nfs4 defaults 0 0",
                     "C: Use autofs with /etc/auto.master and /etc/auto.nfs",
                     "D: All of the above"],
                    3, "hard", "Advanced Storage",
                    "Multiple methods exist for NFS automounting",
                    "All methods work: /etc/fstab with _netdev option, NFSv4 in fstab, or autofs for on-demand mounting."
                ),
            ]
        }
        return questions
    
    def select_questions(self):
        """Select 15 questions: 5 easy, 5 medium, 5 hard"""
        easy = random.sample(self.questions_pool['easy'], min(5, len(self.questions_pool['easy'])))
        medium = random.sample(self.questions_pool['medium'], min(5, len(self.questions_pool['medium'])))
        hard = random.sample(self.questions_pool['hard'], min(5, len(self.questions_pool['hard'])))
        self.selected_questions = easy + medium + hard
    
    def display_stats(self):
        """Display current game statistics"""
        print_separator()
        lives_display = "❤️ " * self.lives + "💔 " * (3 - self.lives)
        print_colored(f"  Question: {self.current_question + 1}/15  |  Score: {self.score:,}  |  Lives: {lives_display}", Colors.BOLD)
        
        # Show lifelines
        lifeline_status = []
        lifeline_status.append(f"✂️  50/50 {'✓' if self.lifelines['5050'] else '✗'}")
        lifeline_status.append(f"💡 Hint {'✓' if self.lifelines['hint'] else '✗'}")
        lifeline_status.append(f"⏭️  Skip {'✓' if self.lifelines['skip'] else '✗'}")
        print_colored(f"  Lifelines: {' | '.join(lifeline_status)}", Colors.CYAN)
        print_separator()
    
    def display_question(self, question: Question):
        """Display the current question"""
        print()
        difficulty_colors = {
            'easy': Colors.GREEN,
            'medium': Colors.YELLOW,
            'hard': Colors.RED
        }
        
        print_colored(f"  [{question.difficulty.upper()}]", difficulty_colors[question.difficulty] + Colors.BOLD)
        print_colored(f"  Worth: {self.POINT_VALUES[self.current_question]:,} points", Colors.CYAN)
        print()
        print_colored(f"  {question.question}", Colors.BOLD)
        print()
        
        for option in question.options:
            print(f"    {option}")
        print()
    
    def use_lifeline_5050(self, question: Question) -> List[str]:
        """Use 50/50 lifeline - remove 2 wrong answers"""
        if not self.lifelines['5050']:
            print_colored("  ✗ 50/50 lifeline already used!", Colors.RED)
            return question.options
        
        self.lifelines['5050'] = False
        wrong_indices = [i for i in range(4) if i != question.correct]
        to_remove = random.sample(wrong_indices, 2)
        
        new_options = []
        for i, opt in enumerate(question.options):
            if i in to_remove:
                new_options.append(f"    {opt.split(':')[0]}: [REMOVED]")
            else:
                new_options.append(f"    {opt}")
        
        print_colored("\n  ✂️  50/50 activated! Two wrong answers removed.\n", Colors.YELLOW)
        return new_options
    
    def use_lifeline_hint(self, question: Question):
        """Use hint lifeline"""
        if not self.lifelines['hint']:
            print_colored("  ✗ Hint lifeline already used!", Colors.RED)
            return
        
        self.lifelines['hint'] = False
        print_colored(f"\n  💡 Hint: {question.hint}\n", Colors.YELLOW)
    
    def use_lifeline_skip(self):
        """Use skip lifeline"""
        if not self.lifelines['skip']:
            print_colored("  ✗ Skip lifeline already used!", Colors.RED)
            return False
        
        self.lifelines['skip'] = False
        print_colored("\n  ⏭️  Question skipped! Moving to next question...\n", Colors.YELLOW)
        time.sleep(1.5)
        return True
    
    def get_answer(self, question: Question) -> Tuple[str, bool]:
        """Get player's answer with lifeline options"""
        while True:
            print_colored("  Your answer (A/B/C/D) or lifeline (1=50/50, 2=Hint, 3=Skip): ", Colors.BOLD, end='')
            choice = input().strip().upper()
            
            if choice == '1':
                modified_options = self.use_lifeline_5050(question)
                print()
                for opt in modified_options:
                    print(opt)
                print()
                continue
            elif choice == '2':
                self.use_lifeline_hint(question)
                continue
            elif choice == '3':
                if self.use_lifeline_skip():
                    return None, True  # Skipped
                continue
            elif choice in ['A', 'B', 'C', 'D']:
                return choice, False
            else:
                print_colored("  Invalid input! Please enter A, B, C, D, or 1, 2, 3 for lifelines.", Colors.RED)
    
    def check_answer(self, question: Question, answer: str) -> bool:
        """Check if answer is correct"""
        correct_letter = ['A', 'B', 'C', 'D'][question.correct]
        return answer == correct_letter
    
    def play_round(self):
        """Play a single round"""
        question = self.selected_questions[self.current_question]
        
        clear_screen()
        print_banner()
        self.display_stats()
        self.display_question(question)
        
        answer, skipped = self.get_answer(question)
        
        if skipped:
            self.answers_history.append({
                'question': question.question,
                'your_answer': 'SKIPPED',
                'correct': True,
                'topic': question.topic,
                'explanation': question.explanation
            })
            return True
        
        is_correct = self.check_answer(question, answer)
        
        # Record answer
        self.answers_history.append({
            'question': question.question,
            'your_answer': answer,
            'correct_answer': ['A', 'B', 'C', 'D'][question.correct],
            'correct': is_correct,
            'topic': question.topic,
            'explanation': question.explanation
        })
        
        # Update topic stats
        if question.topic not in self.topic_stats:
            self.topic_stats[question.topic] = {'correct': 0, 'total': 0}
        self.topic_stats[question.topic]['total'] += 1
        
        print()
        if is_correct:
            self.topic_stats[question.topic]['correct'] += 1
            points_earned = self.POINT_VALUES[self.current_question]
            self.score += points_earned
            print_colored(f"  ✓ CORRECT! +{points_earned:,} points", Colors.GREEN + Colors.BOLD)
            print_colored(f"  {question.explanation}", Colors.CYAN)
            time.sleep(2)
            return True
        else:
            self.lives -= 1
            correct_letter = ['A', 'B', 'C', 'D'][question.correct]
            print_colored(f"  ✗ WRONG! The correct answer was {correct_letter}", Colors.RED + Colors.BOLD)
            print_colored(f"  {question.explanation}", Colors.CYAN)
            print_colored(f"  Lives remaining: {self.lives}", Colors.YELLOW)
            time.sleep(3)
            
            if self.lives == 0:
                return False
            
            # Check safe haven
            if self.current_question + 1 in self.SAFE_HAVENS:
                safe_score = 5000 if self.current_question + 1 == 5 else 50000
                if self.score < safe_score:
                    self.score = safe_score
                    print_colored(f"\n  💰 Safe Haven! Your score is guaranteed at {safe_score:,} points", Colors.GREEN + Colors.BOLD)
                    time.sleep(2)
            
            return True
    
    def show_final_stats(self):
        """Display final game statistics"""
        clear_screen()
        print_banner()
        print_separator()
        
        if self.current_question >= 15:
            print_colored("\n  🎉 CONGRATULATIONS! YOU'RE AN RHCSA MASTER! 🎉\n", Colors.GREEN + Colors.BOLD)
        elif self.lives == 0:
            print_colored("\n  💔 GAME OVER - Out of Lives 💔\n", Colors.RED + Colors.BOLD)
        else:
            print_colored("\n  🎮 GAME ENDED 🎮\n", Colors.YELLOW + Colors.BOLD)
        
        print_colored(f"  Final Score: {self.score:,} points", Colors.CYAN + Colors.BOLD)
        print_colored(f"  Questions Answered: {self.current_question}/15", Colors.CYAN)
        
        correct_answers = sum(1 for a in self.answers_history if a['correct'])
        accuracy = (correct_answers / len(self.answers_history) * 100) if self.answers_history else 0
        print_colored(f"  Accuracy: {accuracy:.1f}%", Colors.CYAN)
        
        print_separator()
        print_colored("\n  📊 Topic Performance:\n", Colors.BOLD)
        
        for topic, stats in sorted(self.topic_stats.items()):
            percentage = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            bar_length = int(percentage / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            color = Colors.GREEN if percentage >= 70 else Colors.YELLOW if percentage >= 50 else Colors.RED
            print_colored(f"  {topic:.<30} {stats['correct']}/{stats['total']} [{bar}] {percentage:.0f}%", color)
        
        print_separator()
    
    def review_answers(self):
        """Show detailed review of all answers"""
        print_colored("\n  📝 Answer Review:\n", Colors.BOLD)
        
        for i, answer in enumerate(self.answers_history, 1):
            status = "✓" if answer['correct'] else "✗"
            color = Colors.GREEN if answer['correct'] else Colors.RED
            
            print_colored(f"\n  {i}. {answer['question']}", Colors.BOLD)
            if answer['your_answer'] == 'SKIPPED':
                print_colored(f"     {status} SKIPPED", Colors.YELLOW)
            else:
                print_colored(f"     {status} Your answer: {answer['your_answer']}", color)
                if not answer['correct']:
                    print_colored(f"     ✓ Correct answer: {answer['correct_answer']}", Colors.GREEN)
            print_colored(f"     💡 {answer['explanation']}", Colors.CYAN)
        
        print()
    
    def play(self):
        """Main game loop"""
        clear_screen()
        print_banner()
        
        print_colored("\n  Welcome to RHCSA Millionaire!", Colors.BOLD)
        print("\n  Answer 15 questions about Red Hat Enterprise Linux system administration.")
        print("  Questions get harder, but you earn more points!")
        print("\n  Rules:")
        print("  • You have 3 lives - lose one for each wrong answer")
        print("  • Safe havens at questions 5 (5,000 pts) and 10 (50,000 pts)")
        print("  • Use lifelines wisely: 50/50, Hint, and Skip")
        print("  • Reach 1,000,000 points to become an RHCSA Master!")
        
        print_colored("\n  Press Enter to start...", Colors.YELLOW)
        input()
        
        self.select_questions()
        
        while self.current_question < 15 and self.lives > 0:
            if not self.play_round():
                break
            self.current_question += 1
        
        self.show_final_stats()
        
        print_colored("\n  Would you like to review your answers? (y/n): ", Colors.BOLD, end='')
        if input().strip().lower() == 'y':
            self.review_answers()
        
        print_colored("\n  Thanks for playing RHCSA Millionaire!", Colors.CYAN + Colors.BOLD)
        print_colored("  Good luck on your EX200 exam! 🎓\n", Colors.GREEN)

def main():
    """Main entry point"""
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        print_colored("\n\n  Game interrupted. Thanks for playing!", Colors.YELLOW)
        sys.exit(0)

if __name__ == "__main__":
    main()