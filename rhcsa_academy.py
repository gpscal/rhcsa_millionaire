#!/usr/bin/env python3
"""
RHCSA Academy - Interactive Learning Platform for EX200 Exam Preparation
Comprehensive course based on real RHCSA exam questions with progress tracking
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# ANSI color codes
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

def print_separator(char='═', length=70):
    """Print a separator line"""
    print_colored(char * length, Colors.BLUE)

def print_banner():
    """Display the application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                 🎓 RHCSA ACADEMY 🎓                              ║
    ║                                                                  ║
    ║          Interactive Learning Platform for EX200 Exam           ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN + Colors.BOLD)

def wait_for_enter(message="Press Enter to continue..."):
    """Wait for user to press Enter"""
    print_colored(f"\n  {message}", Colors.YELLOW)
    input()

class Lesson:
    """Represents a single lesson within a module"""
    def __init__(self, title: str, theory: str, example: str, 
                 commands: List[str], tips: List[str], exam_question: str, 
                 exam_solution: str, practice_tasks: List[str]):
        self.title = title
        self.theory = theory
        self.example = example
        self.commands = commands
        self.tips = tips
        self.exam_question = exam_question
        self.exam_solution = exam_solution
        self.practice_tasks = practice_tasks

class Quiz:
    """Represents a quiz question"""
    def __init__(self, question: str, options: List[str], 
                 correct: int, explanation: str):
        self.question = question
        self.options = options
        self.correct = correct
        self.explanation = explanation

class Module:
    """Represents a learning module"""
    def __init__(self, id: str, title: str, description: str, 
                 difficulty: str, lessons: List[Lesson], quiz: List[Quiz]):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.lessons = lessons
        self.quiz = quiz

class ProgressTracker:
    """Tracks and persists user progress"""
    def __init__(self, progress_file='rhcsa_progress.json'):
        self.progress_file = progress_file
        self.data = self.load_progress()
    
    def load_progress(self) -> Dict:
        """Load progress from JSON file"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                return self.create_new_progress()
        return self.create_new_progress()
    
    def create_new_progress(self) -> Dict:
        """Create new progress structure"""
        return {
            'started_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'modules': {},
            'bookmarks': [],
            'notes': {},
            'quiz_scores': {},
            'completed_lessons': [],
            'total_study_time': 0,
            'achievements': []
        }
    
    def save_progress(self):
        """Save progress to JSON file"""
        self.data['last_accessed'] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def mark_lesson_complete(self, module_id: str, lesson_index: int):
        """Mark a lesson as complete"""
        key = f"{module_id}_{lesson_index}"
        if key not in self.data['completed_lessons']:
            self.data['completed_lessons'].append(key)
        
        if module_id not in self.data['modules']:
            self.data['modules'][module_id] = {
                'started': True,
                'completed_lessons': [],
                'quiz_completed': False
            }
        
        if lesson_index not in self.data['modules'][module_id]['completed_lessons']:
            self.data['modules'][module_id]['completed_lessons'].append(lesson_index)
        
        self.save_progress()
    
    def save_quiz_score(self, module_id: str, score: int, total: int):
        """Save quiz score"""
        self.data['quiz_scores'][module_id] = {
            'score': score,
            'total': total,
            'percentage': (score / total * 100) if total > 0 else 0,
            'date': datetime.now().isoformat()
        }
        if module_id in self.data['modules']:
            self.data['modules'][module_id]['quiz_completed'] = True
        self.save_progress()
    
    def add_bookmark(self, module_id: str, lesson_index: int, note: str = ""):
        """Add a bookmark"""
        bookmark = {
            'module_id': module_id,
            'lesson_index': lesson_index,
            'note': note,
            'date': datetime.now().isoformat()
        }
        self.data['bookmarks'].append(bookmark)
        self.save_progress()
    
    def add_note(self, module_id: str, lesson_index: int, note: str):
        """Add a note"""
        key = f"{module_id}_{lesson_index}"
        if key not in self.data['notes']:
            self.data['notes'][key] = []
        self.data['notes'][key].append({
            'note': note,
            'date': datetime.now().isoformat()
        })
        self.save_progress()
    
    def get_module_progress(self, module_id: str, total_lessons: int) -> Dict:
        """Get progress for a specific module"""
        if module_id not in self.data['modules']:
            return {'completed': 0, 'total': total_lessons, 'percentage': 0}
        
        completed = len(self.data['modules'][module_id]['completed_lessons'])
        return {
            'completed': completed,
            'total': total_lessons,
            'percentage': (completed / total_lessons * 100) if total_lessons > 0 else 0
        }
    
    def get_overall_progress(self, total_modules: int) -> Dict:
        """Get overall progress"""
        completed_modules = sum(1 for m in self.data['modules'].values() 
                               if m.get('quiz_completed', False))
        return {
            'completed_modules': completed_modules,
            'total_modules': total_modules,
            'percentage': (completed_modules / total_modules * 100) if total_modules > 0 else 0,
            'total_lessons_completed': len(self.data['completed_lessons'])
        }

class RHCSAAcademy:
    """Main application class"""
    
    def __init__(self):
        self.progress = ProgressTracker()
        self.modules = self.load_curriculum()
        self.current_module = None
        self.current_lesson = None
    
    def load_curriculum(self) -> List[Module]:
        """Load all learning modules based on real exam content"""
        return [
            # Module 1: System Recovery and Boot Process
            Module(
                id="module_01",
                title="System Recovery and Boot Process",
                description="Master root password reset, GRUB configuration, and boot targets",
                difficulty="Critical",
                lessons=[
                    Lesson(
                        title="Resetting Root Password from Rescue Mode",
                        theory="""
Understanding how to reset the root password is CRITICAL for the RHCSA exam.
This is often the FIRST task you'll encounter, as you may be locked out initially.

KEY CONCEPTS:
1. Interrupt boot process at GRUB menu
2. Enter emergency/rescue mode
3. Remount root filesystem as read-write
4. Use chroot to change root context
5. Change password and handle SELinux relabeling

This procedure works because:
- The system boots with minimal services
- Root filesystem is mounted read-only at /sysroot
- chroot changes the root directory context
- SELinux must relabel files after password change
                        """,
                        example="""
REAL EXAM SCENARIO:
You boot the system and realize you don't know the root password.
You have physical access to the machine.

STEP-BY-STEP PROCEDURE:
1. Reboot the system
2. At GRUB menu, press 'e' to edit boot entry
3. Find the line starting with 'linux' or 'linux16'
4. Go to the end of that line
5. Add: rd.break
6. (For RHEL 8+) Remove: ro and crashkernel parameters
7. Press Ctrl+x to boot
                        """,
                        commands=[
                            "# At rescue prompt:",
                            "mount -o remount,rw /sysroot",
                            "chroot /sysroot",
                            "passwd root",
                            "# Enter new password twice",
                            "touch /.autorelabel",
                            "exit",
                            "exit",
                            "# System will reboot and relabel"
                        ],
                        tips=[
                            "ALWAYS create /.autorelabel - this triggers SELinux relabeling",
                            "Alternative to touch /.autorelabel: load_policy -i && chcon -t shadow_t /etc/shadow",
                            "The system will reboot twice (once for relabel)",
                            "Don't forget to press 'e' at GRUB, not Enter",
                            "rd.break stops boot BEFORE root is mounted on /"
                        ],
                        exam_question="""
EXAM TASK:
You do not know the root password but you have physical access to the machine.
Reset the root password to 'redhat' and log into the system.
                        """,
                        exam_solution="""
COMPLETE SOLUTION:
1. Reboot system
2. At GRUB menu, press 'e'
3. Find linux line, go to end
4. Add: rd.break
5. Remove: ro crashkernel=auto (if present)
6. Ctrl+x to boot
7. Execute:
   mount -o remount,rw /sysroot
   chroot /sysroot
   passwd root
   (enter 'redhat' twice)
   touch /.autorelabel
   exit
   exit
8. Wait for system to reboot and relabel
9. Login as root with password 'redhat'

VERIFICATION:
- You should be able to login with new password
- Check: ls -Z /etc/shadow (correct SELinux context)
                        """,
                        practice_tasks=[
                            "Practice this procedure in a VM until you can do it in under 3 minutes",
                            "Try alternative SELinux method: load_policy -i && chcon -t shadow_t /etc/shadow",
                            "Intentionally skip /.autorelabel and see what happens (learning experience)",
                            "Document each step in your own words"
                        ]
                    ),
                    Lesson(
                        title="GRUB Configuration and Kernel Parameters",
                        theory="""
GRUB (GRand Unified Bootloader) is the bootloader for RHEL systems.
Understanding GRUB is essential for:
- Adding kernel parameters permanently
- Troubleshooting boot issues
- Changing default kernel
- Setting boot targets

TWO METHODS FOR KERNEL PARAMETERS:
1. Temporary (one boot): Edit at GRUB menu
2. Permanent: Edit /etc/default/grub OR use grubby command

IMPORTANT LOCATIONS:
- /etc/default/grub - Main GRUB configuration
- /boot/grub2/grub.cfg - Generated GRUB config (BIOS)
- /boot/efi/EFI/redhat/grub.cfg - Generated GRUB config (UEFI)
- Never edit grub.cfg directly!
                        """,
                        example="""
TEMPORARY KERNEL PARAMETER (for current boot only):
1. At GRUB menu, press 'e'
2. Find linux line
3. Add parameter at end (e.g., 'quiet', 'systemd.unit=rescue.target')
4. Ctrl+x to boot

PERMANENT KERNEL PARAMETER - Method 1 (grubby):
grubby --update-kernel=ALL --args='quiet'
grubby --update-kernel=ALL --remove-args='rhgb'
grubby --info=ALL  # Verify changes

PERMANENT KERNEL PARAMETER - Method 2 (grub file):
1. Edit /etc/default/grub
2. Modify GRUB_CMDLINE_LINUX="..." line
3. Add your parameters inside the quotes
4. Regenerate grub.cfg:
   BIOS: grub2-mkconfig -o /boot/grub2/grub.cfg
   UEFI: grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
                        """,
                        commands=[
                            "# View all installed kernels",
                            "grubby --info=ALL",
                            "",
                            "# Add parameter to all kernels",
                            "grubby --update-kernel=ALL --args='parameter_name=value'",
                            "",
                            "# Remove parameter from all kernels",
                            "grubby --update-kernel=ALL --remove-args='parameter_name'",
                            "",
                            "# Set default kernel (by index)",
                            "grubby --set-default-index=0",
                            "",
                            "# Alternative: Edit /etc/default/grub",
                            "vi /etc/default/grub",
                            "# Modify GRUB_CMDLINE_LINUX line",
                            "grub2-mkconfig -o /boot/grub2/grub.cfg"
                        ],
                        tips=[
                            "grubby is safer than editing grub.cfg directly",
                            "Both methods (grubby and /etc/default/grub) are acceptable on exam",
                            "For UEFI systems, grub.cfg is in /boot/efi/EFI/redhat/",
                            "Check with 'cat /proc/cmdline' to see active kernel parameters",
                            "Kernel updates don't replace old kernels - they're added alongside"
                        ],
                        exam_question="""
EXAM TASK:
Add the kernel parameter 'quiet' to all installed kernels permanently.
Ensure the change survives system reboots.
                        """,
                        exam_solution="""
METHOD 1 (Recommended - using grubby):
grubby --update-kernel=ALL --args='quiet'
grubby --info=ALL  # Verify the change
reboot  # Test

METHOD 2 (Using GRUB configuration file):
vi /etc/default/grub
# Find line: GRUB_CMDLINE_LINUX="..."
# Add 'quiet' inside the quotes
# Save and exit
grub2-mkconfig -o /boot/grub2/grub.cfg
# (Or for UEFI: grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg)
reboot  # Test

VERIFICATION:
cat /proc/cmdline  # Should show 'quiet' parameter
                        """,
                        practice_tasks=[
                            "Add a parameter, verify with cat /proc/cmdline, then remove it",
                            "List all kernels with grubby --info=ALL",
                            "Practice both methods (grubby and /etc/default/grub)",
                            "Learn to identify BIOS vs UEFI systems"
                        ]
                    ),
                    Lesson(
                        title="Boot Targets and System Runlevels",
                        theory="""
SYSTEMD TARGETS replace old System V runlevels.
Targets define what services and processes should start at boot.

COMMON TARGETS:
- poweroff.target (runlevel 0): Shutdown
- rescue.target (runlevel 1): Single-user rescue mode
- multi-user.target (runlevels 2,3,4): Multi-user, no GUI
- graphical.target (runlevel 5): Multi-user with GUI
- reboot.target (runlevel 6): Reboot

DEFAULT TARGET:
The system boots into the default target defined by a symlink.
                        """,
                        example="""
VIEWING AND CHANGING BOOT TARGETS:

View current target:
systemctl get-default

Set default to multi-user (no GUI):
systemctl set-default multi-user.target

Set default to graphical (with GUI):
systemctl set-default graphical.target

Change target without rebooting:
systemctl isolate rescue.target
systemctl isolate graphical.target

What systemctl set-default actually does:
It creates a symlink:
/etc/systemd/system/default.target -> /lib/systemd/system/multi-user.target
                        """,
                        commands=[
                            "# View current default target",
                            "systemctl get-default",
                            "",
                            "# Set graphical target (with GUI)",
                            "systemctl set-default graphical.target",
                            "",
                            "# Set multi-user target (no GUI)",
                            "systemctl set-default multi-user.target",
                            "",
                            "# Switch to target immediately (without reboot)",
                            "systemctl isolate multi-user.target",
                            "",
                            "# View all available targets",
                            "systemctl list-units --type=target",
                            "",
                            "# Boot into rescue mode (at GRUB)",
                            "# Add to kernel line: systemd.unit=rescue.target"
                        ],
                        tips=[
                            "systemctl set-default makes the change permanent",
                            "systemctl isolate changes immediately but isn't permanent alone",
                            "Old /etc/inittab is deprecated and doesn't work in RHEL 7+",
                            "You can boot into any target from GRUB by adding systemd.unit=target.name",
                            "rescue.target is useful for troubleshooting"
                        ],
                        exam_question="""
EXAM TASK:
Set the default target to boot into X Window level (graphical interface).
Verify the change without rebooting.
                        """,
                        exam_solution="""
SOLUTION:
systemctl set-default graphical.target
systemctl get-default  # Verify - should show graphical.target

ALTERNATIVE VERIFICATION:
ls -l /etc/systemd/system/default.target
# Should link to /lib/systemd/system/graphical.target

To switch immediately (optional):
systemctl isolate graphical.target

WHAT THE EXAM EXPECTS:
- Default target set to graphical.target
- System boots into GUI after reboot
- Command verification shows correct target
                        """,
                        practice_tasks=[
                            "Switch between multi-user and graphical targets",
                            "Use systemctl isolate to switch without reboot",
                            "Verify the symlink created by set-default",
                            "Practice booting into rescue mode from GRUB"
                        ]
                    )
                ],
                quiz=[
                    Quiz(
                        "What is the correct first step when resetting root password from rescue mode?",
                        [
                            "A: chroot /sysroot",
                            "B: mount -o remount,rw /sysroot",
                            "C: passwd root",
                            "D: touch /.autorelabel"
                        ],
                        1,
                        "You must first remount /sysroot as read-write before you can make any changes. The default mount is read-only."
                    ),
                    Quiz(
                        "Why is creating /.autorelabel necessary after changing root password?",
                        [
                            "A: To make the password change permanent",
                            "B: To fix SELinux contexts on /etc/shadow",
                            "C: To enable root login",
                            "D: To reboot the system"
                        ],
                        1,
                        "Changing the password modifies /etc/shadow, which needs proper SELinux context. .autorelabel triggers full system relabeling on next boot."
                    ),
                    Quiz(
                        "Which command makes a kernel parameter change permanent?",
                        [
                            "A: grubby --update-kernel=ALL --args='parameter'",
                            "B: echo 'parameter' > /proc/cmdline",
                            "C: systemctl set-param parameter",
                            "D: modprobe parameter"
                        ],
                        0,
                        "grubby --update-kernel=ALL --args= updates kernel parameters permanently across all kernels. Editing /etc/default/grub also works."
                    ),
                    Quiz(
                        "What does 'systemctl set-default multi-user.target' actually do?",
                        [
                            "A: Immediately switches to multi-user mode",
                            "B: Creates a symlink at /etc/systemd/system/default.target",
                            "C: Modifies /etc/inittab",
                            "D: Disables the GUI"
                        ],
                        1,
                        "It creates a symlink from default.target to multi-user.target. The system will boot into this target after reboot."
                    ),
                    Quiz(
                        "How do you boot into rescue mode from GRUB for troubleshooting?",
                        [
                            "A: Add 'rescue' to kernel line",
                            "B: Add 'systemd.unit=rescue.target' to kernel line",
                            "C: Add 'single' to kernel line",
                            "D: Add 'init=/bin/bash' to kernel line"
                        ],
                        1,
                        "systemd.unit=rescue.target boots into rescue (single-user) mode. This is useful for emergency repairs."
                    )
                ]
            ),
            
            # Module 2: User and Group Management
            Module(
                id="module_02",
                title="User and Group Management",
                description="Create and manage users, groups, passwords, and account policies",
                difficulty="Essential",
                lessons=[
                    Lesson(
                        title="Creating Users with Specific Properties",
                        theory="""
User management is fundamental to system administration.
RHCSA requires you to create users with specific UIDs, shells, groups, and more.

KEY FILES:
- /etc/passwd: User account information
- /etc/shadow: Encrypted passwords and password policies
- /etc/group: Group information
- /etc/gshadow: Secure group information
- /etc/skel/: Template for new user home directories
- /etc/login.defs: Default settings for user creation

USER CREATION COMMANDS:
- useradd: Create new user (low-level)
- adduser: User-friendly wrapper (symlink to useradd on RHEL)
- usermod: Modify existing user
- userdel: Delete user
                        """,
                        example="""
BASIC USER CREATION:
useradd john
passwd john

CREATE USER WITH SPECIFIC UID:
useradd -u 2000 alice
passwd alice

CREATE USER WITH SPECIFIC GID:
useradd -g 2000 bob
# OR with group name:
useradd -g developers bob

CREATE USER WITHOUT SHELL ACCESS:
useradd -s /sbin/nologin sarah

CREATE USER WITH CUSTOM HOME DIRECTORY:
useradd -d /home/custom/path tom
useradd -m -d /custom/home tom  # -m creates directory

CREATE USER WITH COMMENT:
useradd -c "John Doe - IT Admin" john

CREATE USER WITH EXPIRATION DATE:
useradd -e 2024-12-31 tempuser
                        """,
                        commands=[
                            "# Create user with UID 2000",
                            "useradd -u 2000 john",
                            "passwd john",
                            "",
                            "# Create user with specific GID",
                            "useradd -g developers alice",
                            "",
                            "# Create user without shell",
                            "useradd -s /sbin/nologin sarah",
                            "",
                            "# View user information",
                            "id john",
                            "getent passwd john",
                            "grep john /etc/passwd",
                            "",
                            "# Modify existing user",
                            "usermod -u 3000 john  # Change UID",
                            "usermod -s /bin/bash sarah  # Change shell",
                            "usermod -L john  # Lock account",
                            "usermod -U john  # Unlock account"
                        ],
                        tips=[
                            "Always set a password after creating a user (useradd doesn't set one)",
                            "UIDs below 1000 are typically reserved for system accounts",
                            "/sbin/nologin is used for service accounts that shouldn't have shell access",
                            "Use 'id username' to quickly view user UID, GID, and groups",
                            "usermod -L locks an account by prefixing the password with '!'"
                        ],
                        exam_question="""
EXAM TASK:
Create two users:
- john with UID/GID equal to 2000, password '12345678'
- davis with UID/GID equal to 3000, password '87654321'
Make davis' password validity stop in one month.
                        """,
                        exam_solution="""
COMPLETE SOLUTION:

# Create john
useradd -u 2000 john
passwd john
# Enter: 12345678 (twice)

# Create davis  
useradd -u 3000 davis
passwd davis
# Enter: 87654321 (twice)

# Set davis password to expire in 30 days
chage -E $(date -d +30days +%Y-%m-%d) davis

# OR manually:
chage -E 2024-12-15 davis  # Replace with actual date 30 days from now

VERIFICATION:
id john  # Should show uid=2000
id davis  # Should show uid=3000
chage -l davis  # Should show account expiration date

IMPORTANT NOTES:
- Both users get their own group with matching GID by default
- The date format for chage -E is YYYY-MM-DD
- You can copy the date command from 'man chage' examples
                        """,
                        practice_tasks=[
                            "Create users with different UIDs and verify with 'id' command",
                            "Try to create a user with an already-used UID (it will fail)",
                            "Create a user with /sbin/nologin and try to SSH as that user",
                            "Examine /etc/passwd and /etc/shadow to understand the format"
                        ]
                    ),
                    Lesson(
                        title="Managing Groups and Secondary Groups",
                        theory="""
GROUPS allow you to manage permissions for multiple users collectively.

PRIMARY GROUP vs SECONDARY GROUPS:
- Primary Group: User's main group (specified in /etc/passwd)
- Secondary Groups: Additional groups user belongs to

Every user has exactly ONE primary group but can have MULTIPLE secondary groups.

GROUP COMMANDS:
- groupadd: Create new group
- groupmod: Modify group
- groupdel: Delete group
- groups: Show user's groups
- groupmems: Manage group membership
- gpasswd: Administer groups
                        """,
                        example="""
CREATE GROUP:
groupadd developers
groupadd -g 5000 admins  # With specific GID

ADD USER TO SECONDARY GROUP:
usermod -aG developers john  # -a = append, -G = supplementary groups
# WARNING: Without -a, you REPLACE all secondary groups!

ADD USER TO MULTIPLE GROUPS:
usermod -aG developers,admins,operators john

CHANGE USER'S PRIMARY GROUP:
usermod -g developers john

VIEW USER'S GROUPS:
groups john
id john

VIEW GROUP MEMBERS:
groupmems -g developers -l
getent group developers

REMOVE USER FROM GROUP:
gpasswd -d john developers
                        """,
                        commands=[
                            "# Create group",
                            "groupadd sysgrp",
                            "",
                            "# Create users and add to group",
                            "useradd andrew",
                            "useradd susan",
                            "passwd andrew",
                            "passwd susan",
                            "",
                            "# Add users to secondary group",
                            "usermod -aG sysgrp andrew",
                            "usermod -aG sysgrp susan",
                            "",
                            "# Verify group membership",
                            "groups andrew",
                            "id andrew",
                            "groupmems -g sysgrp -l",
                            "",
                            "# Create user without shell",
                            "useradd sarah -s /sbin/nologin",
                            "passwd sarah",
                            "",
                            "# Try to login as sarah (should fail)",
                            "su - sarah"
                        ],
                        tips=[
                            "ALWAYS use -aG (not just -G) when adding secondary groups",
                            "usermod -G without -a REPLACES all secondary groups (dangerous!)",
                            "Use 'id username' to see all groups including GIDs",
                            "groupmems and gpasswd can both manage membership",
                            "newgrp command temporarily changes user's current primary group"
                        ],
                        exam_question="""
EXAM TASK:
1. Create group 'sysgrp'
2. Create users andrew and susan who belong to this group (as secondary group)
3. Create user sarah who does not have access to the shell
4. Password for all users should be 'Postroll'
                        """,
                        exam_solution="""
COMPLETE SOLUTION:

# Create group
groupadd sysgrp

# Create users
useradd andrew
useradd susan
useradd sarah -s /sbin/nologin

# Set passwords
echo 'Postroll' | passwd --stdin andrew
echo 'Postroll' | passwd --stdin susan  
echo 'Postroll' | passwd --stdin sarah

# OR set passwords interactively:
passwd andrew  # Enter: Postroll
passwd susan   # Enter: Postroll
passwd sarah   # Enter: Postroll

# Add andrew and susan to sysgrp
usermod -aG sysgrp andrew
usermod -aG sysgrp susan

VERIFICATION:
id andrew  # Should show sysgrp in groups
id susan   # Should show sysgrp in groups
id sarah   # Should show shell /sbin/nologin
groupmems -g sysgrp -l  # Should list andrew and susan
su - sarah  # Should fail with "This account is currently not available"
                        """,
                        practice_tasks=[
                            "Create multiple users and a group, add users to group",
                            "Try usermod -G (without -a) and see what happens to secondary groups",
                            "Use newgrp to temporarily change your current group",
                            "Verify group membership with multiple commands (groups, id, getent)"
                        ]
                    ),
                    Lesson(
                        title="Password Policies and Account Expiration",
                        theory="""
PASSWORD AGING controls when passwords must be changed.
This is critical for security and compliance.

KEY CONCEPTS:
- Password expiration: When password must be changed
- Account expiration: When account becomes inaccessible
- Password age minimum: Minimum days before password can be changed
- Warning period: Days before expiration to warn user
- Inactivity period: Days after expiration before account locks

COMMANDS:
- chage: Change user password expiry information
- passwd: Set password and some policies
                        """,
                        example="""
SET PASSWORD TO EXPIRE IN 90 DAYS:
chage -M 90 john
# -M = maximum days password is valid

SET MINIMUM DAYS BETWEEN PASSWORD CHANGES:
chage -m 7 john  
# User must wait 7 days before changing password again

SET WARNING DAYS BEFORE EXPIRATION:
chage -W 14 john
# Warn user 14 days before password expires

SET ACCOUNT EXPIRATION DATE:
chage -E 2024-12-31 john
chage -E $(date -d +30days +%Y-%m-%d) john

SET PASSWORD TO NEVER EXPIRE:
chage -M -1 john

FORCE PASSWORD CHANGE AT NEXT LOGIN:
chage -d 0 john
passwd -e john  # Alternative method

VIEW PASSWORD AGE INFORMATION:
chage -l john
                        """,
                        commands=[
                            "# Set password to expire in 90 days",
                            "chage -M 90 john",
                            "",
                            "# Set minimum days between changes",
                            "chage -m 7 john",
                            "",
                            "# Set warning period",
                            "chage -W 14 john",
                            "",
                            "# Set account expiration (30 days from now)",
                            "chage -E $(date -d +30days +%Y-%m-%d) davis",
                            "",
                            "# Force password change at next login",
                            "chage -d 0 john",
                            "",
                            "# View password age info",
                            "chage -l john",
                            "",
                            "# Lock/unlock account",
                            "passwd -l john  # Lock",
                            "passwd -u john  # Unlock",
                            "",
                            "# Using usermod",
                            "usermod -L john  # Lock",
                            "usermod -U john  # Unlock"
                        ],
                        tips=[
                            "chage -M = Maximum days (password expiration)",
                            "chage -E = Account expiration date (format: YYYY-MM-DD)",
                            "There's a difference between password expiration and account expiration",
                            "Copy date calculation from 'man chage' - no need to memorize",
                            "passwd -l and usermod -L both lock accounts by prefixing password with '!'"
                        ],
                        exam_question="""
EXAM TASK:
Set user 'davis' password to expire in 90 days.
Set the account to expire in 30 days from today.
                        """,
                        exam_solution="""
COMPLETE SOLUTION:

# Set password to expire in 90 days
chage -M 90 davis

# Set account to expire in 30 days
chage -E $(date -d +30days +%Y-%m-%d) davis

VERIFICATION:
chage -l davis

Output should show:
- Maximum number of days between password change: 90
- Account expires: [date 30 days from now]

ALTERNATIVE (if date calculation doesn't work):
# Calculate manually and use:
chage -E 2024-12-15 davis  # Replace with actual date

KEY POINTS:
- Password expiration (-M) vs Account expiration (-E)
- Date format must be YYYY-MM-DD
- You can find the date command syntax in 'man chage'
                        """,
                        practice_tasks=[
                            "Set various password aging policies and verify with chage -l",
                            "Force a user to change password at next login (chage -d 0)",
                            "Practice date calculations for account expiration",
                            "Lock and unlock accounts, verify in /etc/shadow"
                        ]
                    )
                ],
                quiz=[
                    Quiz(
                        "What is the correct command to create a user with UID 2000?",
                        [
                            "A: useradd john -uid 2000",
                            "B: useradd -u 2000 john",
                            "C: adduser john --uid=2000",
                            "D: createuser -u 2000 john"
                        ],
                        1,
                        "useradd -u 2000 john creates a user with UID 2000. The -u flag specifies the user ID."
                    ),
                    Quiz(
                        "Why must you use -aG instead of just -G when adding secondary groups?",
                        [
                            "A: -aG is faster",
                            "B: -G alone replaces all secondary groups",
                            "C: -aG creates the group if it doesn't exist",
                            "D: -G only works for primary groups"
                        ],
                        1,
                        "Using -G without -a replaces ALL secondary groups. -aG appends to existing groups. This is a common mistake!"
                    ),
                    Quiz(
                        "What does 'chage -M 90 john' do?",
                        [
                            "A: Sets account to expire in 90 days",
                            "B: Sets password to expire in 90 days",
                            "C: Sets minimum 90 days between password changes",
                            "D: Warns user 90 days before expiration"
                        ],
                        1,
                        "chage -M sets the maximum number of days a password is valid. After 90 days, the password must be changed."
                    ),
                    Quiz(
                        "Which shell prevents a user from logging in interactively?",
                        [
                            "A: /bin/false",
                            "B: /bin/bash",
                            "C: /sbin/nologin",
                            "D: Both A and C"
                        ],
                        3,
                        "Both /bin/false and /sbin/nologin prevent interactive login. /sbin/nologin shows a message, /bin/false just exits."
                    ),
                    Quiz(
                        "What's the difference between 'passwd -l' and 'userdel'?",
                        [
                            "A: They do the same thing",
                            "B: passwd -l locks account, userdel deletes it",
                            "C: passwd -l is temporary, userdel is permanent",
                            "D: passwd -l is for passwords only"
                        ],
                        1,
                        "passwd -l locks the account (can be unlocked). userdel permanently deletes the user. Locking is safer for troubleshooting."
                    )
                ]
            )
            
            # Additional modules would follow the same pattern...
            # Module 3: File Permissions and ACLs
            # Module 4: Storage Management (LVM, Partitions, Filesystems)
            # Module 5: SELinux
            # Module 6: Networking
            # Module 7: System Services
            # Module 8: Containers
            # etc...
        ]
    
    def display_main_menu(self):
        """Display main navigation menu"""
        clear_screen()
        print_banner()
        
        overall = self.progress.get_overall_progress(len(self.modules))
        
        print_separator()
        print_colored(f"  📚 Overall Progress: {overall['completed_modules']}/{overall['total_modules']} modules completed", Colors.CYAN)
        print_colored(f"  📖 Total Lessons Completed: {overall['total_lessons_completed']}", Colors.CYAN)
        print_colored(f"  🎯 Completion: {overall['percentage']:.1f}%", Colors.GREEN if overall['percentage'] > 50 else Colors.YELLOW)
        print_separator()
        
        print("\n  📋 MAIN MENU\n")
        print("  1. 📚 Browse Modules")
        print("  2. 📊 View Progress Dashboard")
        print("  3. 🔖 View Bookmarks")
        print("  4. 📝 View Notes")
        print("  5. 🎯 Practice Quiz Mode")
        print("  6. 🔍 Search Content")
        print("  7. ℹ️  About RHCSA Academy")
        print("  8. 🚪 Exit")
        
        print_separator()
        choice = input("\n  Enter your choice (1-8): ").strip()
        return choice
    
    def browse_modules(self):
        """Display module list"""
        while True:
            clear_screen()
            print_banner()
            print_separator()
            print_colored("  📚 LEARNING MODULES", Colors.BOLD)
            print_separator()
            
            for idx, module in enumerate(self.modules, 1):
                progress = self.progress.get_module_progress(module.id, len(module.lessons))
                
                # Color code by difficulty
                diff_color = Colors.RED if module.difficulty == "Critical" else Colors.YELLOW
                
                print(f"\n  {idx}. {module.title}")
                print_colored(f"     Difficulty: {module.difficulty}", diff_color)
                print(f"     {module.description}")
                print_colored(f"     Progress: {progress['completed']}/{progress['total']} lessons ({progress['percentage']:.0f}%)", Colors.CYAN)
                
                # Progress bar
                bar_length = 30
                filled = int(bar_length * progress['percentage'] / 100)
                bar = "█" * filled + "░" * (bar_length - filled)
                print_colored(f"     [{bar}]", Colors.GREEN)
            
            print("\n" + "═" * 70)
            choice = input("\n  Select module (number) or 'b' to go back: ").strip()
            
            if choice.lower() == 'b':
                break
            
            try:
                module_idx = int(choice) - 1
                if 0 <= module_idx < len(self.modules):
                    self.show_module(self.modules[module_idx])
            except ValueError:
                continue
    
    def show_module(self, module: Module):
        """Display module content"""
        while True:
            clear_screen()
            print_banner()
            print_separator()
            print_colored(f"  📖 {module.title}", Colors.BOLD)
            print_colored(f"  {module.description}", Colors.CYAN)
            print_separator()
            
            progress = self.progress.get_module_progress(module.id, len(module.lessons))
            print_colored(f"\n  Progress: {progress['completed']}/{progress['total']} lessons completed", Colors.GREEN)
            
            print("\n  LESSONS:\n")
            for idx, lesson in enumerate(module.lessons):
                completed = f"{module.id}_{idx}" in self.progress.data['completed_lessons']
                status = "✓" if completed else " "
                print(f"  [{status}] {idx + 1}. {lesson.title}")
            
            print(f"\n  [{'✓' if module.id in self.progress.data['quiz_scores'] else ' '}] {len(module.lessons) + 1}. 🎯 Module Quiz")
            
            print("\n" + "═" * 70)
            print("\n  Options:")
            print("  - Enter lesson number to study")
            print("  - Enter 'q' for quiz")
            print("  - Enter 'b' to go back")
            
            choice = input("\n  Your choice: ").strip().lower()
            
            if choice == 'b':
                break
            elif choice == 'q':
                self.take_quiz(module)
            else:
                try:
                    lesson_idx = int(choice) - 1
                    if 0 <= lesson_idx < len(module.lessons):
                        self.study_lesson(module, lesson_idx)
                except ValueError:
                    continue
    
    def study_lesson(self, module: Module, lesson_idx: int):
        """Display and study a lesson"""
        lesson = module.lessons[lesson_idx]
        
        while True:
            clear_screen()
            print_banner()
            print_separator()
            print_colored(f"  📖 {module.title} - Lesson {lesson_idx + 1}", Colors.BOLD)
            print_colored(f"  {lesson.title}", Colors.CYAN)
            print_separator()
            
            print("\n  📋 THEORY\n")
            print(lesson.theory)
            
            print("\n" + "═" * 70)
            print_colored("\n  💡 REAL EXAM EXAMPLE\n", Colors.YELLOW + Colors.BOLD)
            print(lesson.example)
            
            print("\n" + "═" * 70)
            print_colored("\n  ⚡ COMMANDS TO KNOW\n", Colors.GREEN + Colors.BOLD)
            for cmd in lesson.commands:
                print(f"  {cmd}")
            
            print("\n" + "═" * 70)
            print_colored("\n  💡 EXAM TIPS\n", Colors.YELLOW + Colors.BOLD)
            for tip in lesson.tips:
                print(f"  • {tip}")
            
            wait_for_enter("Press Enter to see exam question...")
            
            clear_screen()
            print_banner()
            print_separator()
            print_colored("  📝 EXAM QUESTION", Colors.RED + Colors.BOLD)
            print_separator()
            print(lesson.exam_question)
            
            wait_for_enter("Press Enter to see solution...")
            
            clear_screen()
            print_banner()
            print_separator()
            print_colored("  ✅ COMPLETE SOLUTION", Colors.GREEN + Colors.BOLD)
            print_separator()
            print(lesson.exam_solution)
            
            print("\n" + "═" * 70)
            print_colored("\n  🏋️ PRACTICE TASKS\n", Colors.CYAN + Colors.BOLD)
            for task in lesson.practice_tasks:
                print(f"  • {task}")
            
            print("\n" + "═" * 70)
            print("\n  Options:")
            print("  1. ✓ Mark as completed")
            print("  2. 🔖 Bookmark this lesson")
            print("  3. 📝 Add note")
            print("  4. 📖 Review lesson again")
            print("  5. ← Back to module")
            
            choice = input("\n  Your choice: ").strip()
            
            if choice == '1':
                self.progress.mark_lesson_complete(module.id, lesson_idx)
                print_colored("\n  ✓ Lesson marked as complete!", Colors.GREEN)
                time.sleep(1)
            elif choice == '2':
                note = input("\n  Enter bookmark note (optional): ").strip()
                self.progress.add_bookmark(module.id, lesson_idx, note)
                print_colored("\n  🔖 Lesson bookmarked!", Colors.GREEN)
                time.sleep(1)
            elif choice == '3':
                note = input("\n  Enter your note: ").strip()
                if note:
                    self.progress.add_note(module.id, lesson_idx, note)
                    print_colored("\n  📝 Note saved!", Colors.GREEN)
                    time.sleep(1)
            elif choice == '4':
                continue
            elif choice == '5':
                break
    
    def take_quiz(self, module: Module):
        """Take module quiz"""
        clear_screen()
        print_banner()
        print_separator()
        print_colored(f"  🎯 {module.title} - QUIZ", Colors.BOLD)
        print_separator()
        
        score = 0
        total = len(module.quiz)
        
        for idx, quiz in enumerate(module.quiz, 1):
            print(f"\n  Question {idx} of {total}:")
            print(f"  {quiz.question}\n")
            
            for option in quiz.options:
                print(f"  {option}")
            
            answer = input("\n  Your answer (A/B/C/D): ").strip().upper()
            
            correct_letter = ['A', 'B', 'C', 'D'][quiz.correct]
            
            if answer == correct_letter:
                score += 1
                print_colored("\n  ✓ Correct!", Colors.GREEN)
            else:
                print_colored(f"\n  ✗ Wrong! Correct answer: {correct_letter}", Colors.RED)
            
            print_colored(f"\n  💡 Explanation: {quiz.explanation}", Colors.CYAN)
            
            if idx < total:
                wait_for_enter()
                clear_screen()
                print_banner()
                print_separator()
                print_colored(f"  🎯 {module.title} - QUIZ", Colors.BOLD)
                print_separator()
        
        # Save score
        self.progress.save_quiz_score(module.id, score, total)
        
        percentage = (score / total * 100) if total > 0 else 0
        
        print("\n" + "═" * 70)
        print_colored(f"\n  QUIZ COMPLETE!", Colors.BOLD)
        print_colored(f"  Score: {score}/{total} ({percentage:.1f}%)", Colors.GREEN if percentage >= 70 else Colors.YELLOW)
        
        if percentage >= 90:
            print_colored("\n  🏆 Excellent! You've mastered this module!", Colors.GREEN)
        elif percentage >= 70:
            print_colored("\n  👍 Good job! Consider reviewing incorrect answers.", Colors.YELLOW)
        else:
            print_colored("\n  📚 Keep studying! Review the lessons and try again.", Colors.RED)
        
        wait_for_enter()
    
    def show_progress_dashboard(self):
        """Display comprehensive progress dashboard"""
        clear_screen()
        print_banner()
        print_separator()
        print_colored("  📊 PROGRESS DASHBOARD", Colors.BOLD)
        print_separator()
        
        overall = self.progress.get_overall_progress(len(self.modules))
        
        print(f"\n  🎯 Overall Completion: {overall['percentage']:.1f}%")
        print(f"  📚 Modules Completed: {overall['completed_modules']}/{overall['total_modules']}")
        print(f"  📖 Total Lessons Completed: {overall['total_lessons_completed']}")
        
        print("\n  📈 Module-by-Module Progress:\n")
        
        for module in self.modules:
            progress = self.progress.get_module_progress(module.id, len(module.lessons))
            bar_length = 30
            filled = int(bar_length * progress['percentage'] / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            color = Colors.GREEN if progress['percentage'] == 100 else Colors.YELLOW
            print(f"  {module.title[:40]:.<40} {progress['completed']}/{progress['total']}")
            print_colored(f"  [{bar}] {progress['percentage']:.0f}%", color)
            
            # Quiz score if available
            if module.id in self.progress.data['quiz_scores']:
                quiz = self.progress.data['quiz_scores'][module.id]
                print_colored(f"  Quiz: {quiz['score']}/{quiz['total']} ({quiz['percentage']:.1f}%)", Colors.CYAN)
            print()
        
        print("═" * 70)
        
        if self.progress.data['bookmarks']:
            print(f"\n  🔖 Bookmarks: {len(self.progress.data['bookmarks'])}")
        
        if self.progress.data['notes']:
            print(f"  📝 Notes: {sum(len(notes) for notes in self.progress.data['notes'].values())}")
        
        started = datetime.fromisoformat(self.progress.data['started_at'])
        print(f"\n  📅 Started: {started.strftime('%Y-%m-%d %H:%M')}")
        last = datetime.fromisoformat(self.progress.data['last_accessed'])
        print(f"  🕐 Last Accessed: {last.strftime('%Y-%m-%d %H:%M')}")
        
        wait_for_enter()
    
    def show_bookmarks(self):
        """Display user bookmarks"""
        clear_screen()
        print_banner()
        print_separator()
        print_colored("  🔖 YOUR BOOKMARKS", Colors.BOLD)
        print_separator()
        
        if not self.progress.data['bookmarks']:
            print("\n  No bookmarks yet. Bookmark lessons as you study!")
            wait_for_enter()
            return
        
        for idx, bookmark in enumerate(self.progress.data['bookmarks'], 1):
            module = next((m for m in self.modules if m.id == bookmark['module_id']), None)
            if module and bookmark['lesson_index'] < len(module.lessons):
                lesson = module.lessons[bookmark['lesson_index']]
                print(f"\n  {idx}. {module.title} - {lesson.title}")
                if bookmark['note']:
                    print_colored(f"     Note: {bookmark['note']}", Colors.CYAN)
                date = datetime.fromisoformat(bookmark['date'])
                print(f"     Added: {date.strftime('%Y-%m-%d %H:%M')}")
        
        wait_for_enter()
    
    def run(self):
        """Main application loop"""
        clear_screen()
        print_banner()
        print_colored("\n  Welcome to RHCSA Academy!", Colors.BOLD)
        print("\n  Your comprehensive interactive learning platform for")
        print("  Red Hat Certified System Administrator (EX200) exam preparation.")
        print("\n  ✓ Based on real exam questions")
        print("  ✓ Progress tracking and bookmarks")
        print("  ✓ Hands-on practice tasks")
        print("  ✓ Module quizzes")
        
        wait_for_enter("Press Enter to start your journey...")
        
        while True:
            choice = self.display_main_menu()
            
            if choice == '1':
                self.browse_modules()
            elif choice == '2':
                self.show_progress_dashboard()
            elif choice == '3':
                self.show_bookmarks()
            elif choice == '4':
                print_colored("\n  📝 Notes feature - viewing all notes...", Colors.CYAN)
                wait_for_enter()
            elif choice == '5':
                print_colored("\n  🎯 Practice quiz mode coming soon!", Colors.YELLOW)
                wait_for_enter()
            elif choice == '6':
                print_colored("\n  🔍 Search feature coming soon!", Colors.YELLOW)
                wait_for_enter()
            elif choice == '7':
                self.show_about()
            elif choice == '8':
                clear_screen()
                print_colored("\n  Thank you for using RHCSA Academy!", Colors.GREEN)
                print_colored("  Good luck on your EX200 exam! 🎓\n", Colors.CYAN)
                break
    
    def show_about(self):
        """Show about information"""
        clear_screen()
        print_banner()
        print_separator()
        print_colored("  ℹ️  ABOUT RHCSA ACADEMY", Colors.BOLD)
        print_separator()
        print("""
  RHCSA Academy is an interactive learning platform designed to help you
  prepare for the Red Hat Certified System Administrator (RHCSA) EX200 exam.

  🎯 KEY FEATURES:
  • Curriculum based on REAL exam questions
  • Step-by-step solutions with explanations
  • Automatic progress tracking
  • Bookmarks and notes
  • Module quizzes to test knowledge
  • Practice tasks for hands-on learning

  📚 CONTENT SOURCES:
  • Official RHCSA exam objectives
  • Real exam practice questions
  • Community-contributed study materials
  • Verified solutions and best practices

  💡 STUDY TIPS:
  • Complete lessons in order within each module
  • Practice commands on a real RHEL system
  • Take notes on tricky concepts
  • Review bookmarked lessons before the exam
  • Retake quizzes until you score 90%+

  🏆 EXAM READINESS:
  You're ready when you:
  • Complete all modules with 90%+ quiz scores
  • Can perform tasks without looking at solutions
  • Understand WHY commands work, not just memorize them
  • Complete practice tasks successfully

  Good luck on your certification journey!
        """)
        wait_for_enter()

def main():
    """Main entry point"""
    try:
        academy = RHCSAAcademy()
        academy.run()
    except KeyboardInterrupt:
        print_colored("\n\n  Session interrupted. Your progress has been saved!", Colors.YELLOW)
        sys.exit(0)

if __name__ == "__main__":
    main()
