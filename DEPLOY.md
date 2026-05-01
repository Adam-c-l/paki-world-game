# Deploy Your Private Recoil Lobby Server

This guide will help you deploy your own always-online lobby server for free.

## Recommended: Render (Free, Always-On)

**Render's Background Worker stays always online - perfect for your use case.**

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Name it `recoil-lobby-server`
3. Make it private (recommended)
4. Upload this lobby-server folder to GitHub:

```bash
cd lobby-server
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/recoil-lobby-server.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://dashboard.render.com/
2. Sign up with GitHub
3. Click "New" → "Blueprint"
4. Connect your `recoil-lobby-server` repository
5. Render will read `render.yaml` and create:
   - A background worker (always stays on!)
   - 1GB disk for persistent data
   - Ports 8200 and 8201 exposed

6. Click "Apply"

### Step 3: Get Your Server Address

After deployment:
- Go to your service dashboard
- Copy the service URL (e.g., `recoil-lobby-server-xxx.onrender.com`)
- The lobby runs on **port 8200**

**Your connection address will be:**
```
recoil-lobby-server-xxx.onrender.com:8200
```

### Step 4: Default Accounts (Auto-Created)

**Good news!** The server automatically creates these accounts on first run:
- `player1` / `password1`
- `player2` / `password2`
- `friend` / `friendpass`

### Step 5: Add More Accounts (Optional)

To add custom accounts later:

1. Go to Render dashboard → your service → **Shell**
2. Run: `sqlite3 /app/data/server.db`
3. Add a user with:
```sql
INSERT INTO users (username, password, register_date, last_login, last_ip, access, ingame_time, bot) 
VALUES ('newname', 'newpassword', datetime('now'), datetime('now'), '127.0.0.1', 'user', 0, 0);
```
4. Type `.quit` to exit

## Alternative: Fly.io (Free Tier)

If you prefer Fly.io:

```bash
# Install flyctl from https://fly.io/docs/hands-on/install-flyctl/

# Launch
cd lobby-server
fly launch

# Create persistent volume
fly volumes create lobby_data --size 1

# Deploy
fly deploy
```

## Connect Your Recoil Client

1. Launch Recoil/Chobby
2. Go to **Settings** → **Lobby**
3. Change server from `lobby.springrts.com` to your server address
4. Enter username/password you created
5. Connect!

## For Your Friend to Connect

Your friend needs to:
1. Use the same server address: `your-service.onrender.com:8200`
2. Have their own account (create one for them in the database)
3. Both connect and create/join battles!

## Important Notes

- **Render Background Workers stay always-on** - no sleeping!
- Data persists in the disk volume (accounts, battles, etc.)
- The server runs on port 8200 (lobby) and 8201 (NAT punch)
- SQLite is used (simple, no external DB needed)

## Troubleshooting

**Can't connect?**
- Check Render dashboard logs
- Verify ports 8200/8201 are exposed
- Make sure your account exists in the database

**Friend can't see your battle?**
- Both need to be on the same lobby server
- Check firewall settings
- Try with NAT disabled in battle settings

## Free Forever?

- **Render**: 1 Background Worker + 1GB disk = FREE forever
- Limits: 750 hours/month (more than enough for 1 server)
- For 2 friends playing occasionally, this will never cost money
