# 🎯 RHCSA Millionaire Game Improvements

## Summary of Enhancements

The RHCSA Millionaire game has been significantly enhanced with **comprehensive, real-world exam questions** based on authentic RHCSA study materials and exam guides.

---

## 📊 Question Pool Expansion

### Before:
- **8 Easy Questions**
- **10 Medium Questions**  
- **10 Hard Questions**
- **Total: 28 questions**

### After:
- **17 Easy Questions** (+9)
- **20 Medium Questions** (+10)
- **20 Hard Questions** (+10)
- **Total: 57 questions** (+29 questions, 103% increase!)

---

## 🎓 New Topics & Scenarios Added

### Easy Level (New Questions):
1. **Disk Usage**: `df` command for filesystem space
2. **SELinux Status**: `sestatus` and `getenforce` commands
3. **User Creation**: `useradd` command basics
4. **Network Configuration**: `ip addr` command
5. **Service Management**: `systemctl enable` for auto-start
6. **File Viewing**: `tail` command
7. **Process Control**: Ctrl+C signal handling
8. **File Search**: `find` command introduction
9. **Hostname Management**: Basic system identification

### Medium Level (New Scenarios):
1. **Swap Management**: Creating swap on LVM (`mkswap`, `swapon`)
2. **Custom UID**: Creating users with specific UIDs
3. **ACL Display**: Using `getfacl` to view permissions
4. **File Finding**: `find` with `-mtime` for date-based searches
5. **LVM Extension**: `lvextend` with size increments
6. **Journal Persistence**: Making journald logs survive reboots
7. **YUM Repositories**: Adding repos with `yum-config-manager`
8. **Hostname Configuration**: `hostnamectl` and `/etc/hostname`
9. **Recursive Grep**: `grep -r` for searching in directories
10. **Cron Scheduling**: Daily job configuration syntax
11. **Group Ownership**: `chown` and `chgrp` for groups

### Hard Level (Complex Multi-Step Procedures):
1. **Root Password Reset**: Complete rescue mode procedure with SELinux relabeling
2. **Stratis Storage**: Creating Stratis pools with multiple devices
3. **VDO Configuration**: Setting up VDO volumes with compression ratios
4. **AutoFS NFS**: Configuring autofs for network home directories
5. **Podman User Services**: Container systemd integration with `loginctl enable-linger`
6. **SELinux Permanent Contexts**: Using `semanage fcontext` and `restorecon`
7. **LVM Reduction**: Safe procedure for shrinking ext4 filesystems
8. **Tuned Profiles**: System performance optimization
9. **VDO LVM**: Creating VDO volumes through LVM
10. **Boot Target Configuration**: Multi-user vs graphical target
11. **Temporary Kernel Parameters**: GRUB editor for one-time boot changes
12. **File Finding by UID**: Advanced `find` usage
13. **NFS Fstab**: Proper _netdev configuration for network mounts
14. **SGID Directories**: Collaborative group directories with special permissions

---

## 🔍 Real Exam Scenario Examples

### Example 1: Root Password Reset (Hard)
**Question**: "What is the correct command sequence to reset root password from rescue mode?"

**Correct Answer**: 
```bash
mount -o remount,rw /sysroot && \
chroot /sysroot && \
passwd root && \
touch /.autorelabel
```

**Why This Matters**: This is often the **first task** in RHCSA exams and is critical to know.

---

### Example 2: LVM with XFS Extension (Hard)
**Question**: "What is the correct procedure to extend an XFS filesystem on a logical volume?"

**Correct Answer**:
```bash
lvextend -L +5G /dev/vg/lv && \
xfs_growfs /mount/point
```

**Key Learning**: XFS uses `xfs_growfs` (not `resize2fs`), and it requires the **mount point** not the device path.

---

### Example 3: Podman Container as User Service (Hard)
**Question**: "Which command correctly configures a Podman container to start automatically at boot as a systemd service?"

**Answer**: `podman generate systemd --name mycontainer --files --new`

**Complete Procedure**:
1. Create container
2. Generate systemd unit file
3. Place in `~/.config/systemd/user/`
4. Enable with `systemctl --user enable`
5. Run `loginctl enable-linger` for boot persistence

---

### Example 4: AutoFS for NFS Home Directories (Hard)
**Multi-Step Configuration**:

1. Create `/etc/auto.master.d/home.autofs`:
   ```
   /home/guests /etc/auto.home
   ```

2. Create `/etc/auto.home`:
   ```
   * -rw,sync server:/home/guests/&
   ```

3. Enable service:
   ```bash
   systemctl enable --now autofs
   ```

---

### Example 5: SELinux Permanent Context (Hard)
**Question**: "How do you set SELinux context for a directory permanently?"

**Correct Method**:
```bash
semanage fcontext -a -t httpd_sys_content_t '/web(/.*)?'
restorecon -Rv /web
```

**Wrong Method** (Temporary only):
```bash
chcon -R -t httpd_sys_content_t /web
```

**Key Learning**: `chcon` changes are temporary, `semanage` modifies the policy permanently.

---

## 📚 Sources Used

Questions were derived from:
1. **RHCSA 9 Exam Guide PDF**
2. **Real Exam Questions PDF**
3. **chlebik's RHCSA Practice Questions** (34 scenarios)
4. **SHrEE-7's Practice Exams**
5. **Multiple community-contributed study guides**

All questions reflect **actual exam-style tasks** that candidates encounter.

---

## 🎯 Coverage by RHCSA Exam Objective

### ✅ Understand and Use Essential Tools
- File operations, archiving, compression
- Text processing with grep, find
- File permissions and ACLs
- Remote access and file transfer

### ✅ Operate Running Systems
- Boot process, GRUB configuration
- System targets and runlevels
- Service management with systemd
- Process management and scheduling

### ✅ Configure Local Storage
- Partitioning with MBR/GPT
- LVM (create, extend, reduce, remove)
- File systems (XFS, ext4)
- Swap configuration
- VDO volumes
- Stratis storage

### ✅ Create and Configure File Systems
- Creating and mounting filesystems
- Configuring automount (autofs)
- NFS client configuration
- File system labels and UUIDs
- Persistent mounting via fstab

### ✅ Deploy, Configure, and Maintain Systems
- Package management (dnf/yum)
- Repository configuration
- Kernel updates
- System registration
- Time synchronization

### ✅ Manage Users and Groups
- User and group creation
- Password policies and expiration
- sudo configuration
- Account locking

### ✅ Manage Security
- SELinux modes and contexts
- SELinux booleans
- Firewalld configuration
- SSH configuration
- File permissions and ACLs

### ✅ Manage Containers
- Podman basics
- Container as systemd service
- Persistent containers
- Port mapping and volume mounting
- User namespaces and rootless containers

---

## 🎮 Game Play Improvements

### Enhanced Feedback
- More detailed explanations for each answer
- Real-world context for why commands are used
- Multiple correct approaches highlighted when applicable

### Better Topic Coverage
- Every major RHCSA objective is now represented
- Questions progress from conceptual to hands-on
- Complex multi-step scenarios in hard level

### Randomization Benefits
With 57 total questions and only 15 selected per game:
- **Different experience each play**
- **Encourages multiple practice sessions**
- **Tests broader knowledge base**

---

## 💡 Study Recommendations

### For Easy Questions (100-1,000 pts)
- Focus on command **purpose and basic syntax**
- Memorize file locations (`/etc/passwd`, `/var/log`, etc.)
- Understand service management basics

### For Medium Questions (2,000-32,000 pts)
- Practice **complete task execution**
- Learn flag combinations (`tar -czf`, `nmcli con mod`)
- Understand configuration file locations

### For Hard Questions (64,000-1,000,000 pts)
- Master **multi-step procedures**
- Understand **dependencies** (SELinux relabeling after passwd change)
- Practice **troubleshooting** scenarios
- Know **alternative methods** for same task

---

## 🚀 Next Steps for Practice

After playing the game:

1. **Identify Weak Topics**: Review your topic performance stats
2. **Set Up Lab Environment**: Practice commands on real RHEL system
3. **Follow Procedures**: Execute multi-step scenarios from hard questions
4. **Time Yourself**: RHCSA exam is time-limited (3 hours)
5. **Document Your Work**: Create personal cheat sheets
6. **Play Again**: Different questions each time!

---

## 📈 Success Metrics

To feel confident for the exam:
- **Consistently score 70%+** accuracy
- **Complete all 15 questions** without running out of lives
- **Need minimal hints** on medium/hard questions
- **Can explain** why wrong answers are incorrect
- **Know multiple approaches** for tasks with alternatives

---

## ⚠️ Important Exam Tips

1. **Read Questions Carefully**: Some have multiple correct approaches
2. **Verify Your Work**: Use commands like `mount -a`, `systemctl status`
3. **Check SELinux**: Many failures are SELinux-related
4. **Test After Reboot**: Some tasks require persistence across reboots
5. **Manage Your Time**: Don't spend too long on one question
6. **Use Man Pages**: They're available during the exam!

---

**Happy studying and good luck on your RHCSA exam! 🎓**

*Remember: This game teaches concepts, but hands-on practice is essential for passing the exam.*
