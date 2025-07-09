# Video_Encryption

## Pull the Docker Image using this command:
```
docker pull mohammedfaizal/video_encryption_decryption:v1.0
```

# Running GUI Applications in Docker with Xming (Windows)

## Step 1: Install and Configure Xming
1. Download and install **Xming** or **VcXsrv** from [sourceforge.net](https://sourceforge.net/projects/xming/).
2. Start Xming with the following settings:
   - Multiple Windows
   - Display Number: `0`
   - Enable Native OpenGL
   - Disable Access Control

## Step 2: Set DISPLAY Environment Variable in PowerShell
Open PowerShell and run the following command:
```
$env:DISPLAY="host.docker.internal:0.0"
```
This allows GUI applications inside Docker to communicate with Xming on Windows.

## Step 3: Run the Docker Container with GUI Support
Use the following command to start the container with volume mounting:
Example:`
```
docker run -d --rm --name video_enc_dec -e DISPLAY=host.docker.internal:0.0 -v "C:\Users\SEC\Videos:/app/videos" -it mohammedfaizal/video_encryption_decryption:v1.0
```
### Explanation:
- `-d` → Runs container in **detached mode** (in the background).
- `--name video_enc_dec` → Names the container "video_enc_dec". You can use any name you prefer. Or you can remove "--name video_enc_dec" for random name.
- `-e DISPLAY=host.docker.internal:0.0` → Enables GUI by setting DISPLAY.
- `-v "C:\Users\SEC\Videos:/app/videos"` → Mounts **local folder** (`C:\Users\SEC\Videos`) to **container path** (`/app/videos`). Ensure `C:\Users\SEC\Videos` is replaced with the actual path where your video files are stored.
- `-it mohammedfaizal/video_encryption_decryption:v1.0` → Runs container in interactive mode with the specified image.

## Step 4: Copy Files from Container to Local System
If you need to copy files or folders from the container to your local machine, use the following command:
```
docker cp <container_id or container_name>:<source_path_inside_container> <destination_path_on_host>
```
copy the encrypted and decrypted video files using the `docker cp` command as shown. before stopping the container. Otherwise, the files will be lost when the container is stopped or removed.

### Example:
```
docker cp video_enc_dec:/app/Results C:\Users\SEC\Videos
```
### Explanation:
- `video_enc_dec` → Container name.
- `/app/videos/Results` → Path **inside the container**.
- `C:\Users\SEC\Videos` → Path **on the host machine** to paste the copied files. Ensure `C:\Users\SEC\Videos` is replaced with the actual path where you want to save.

## Step 5: Stop and Start the Container Without Losing Data
If you need to **stop** the container:
```
docker stop video_enc_dec
```
To **start it again** without losing files:
```
docker start -ai video_enc_dec
```

## Step 6: Remove the Container (If Needed)
If you want to delete the container permanently:
```
docker rm video_enc_dec
```

---

### Notes:
- Ensure your Xming or VcXsrv server is running before launching Docker.
- If videos do not appear inside the GUI file selector, ensure they exist in the mounted folder and check the container’s read permissions.
- If you dont want to remove the container after it stops, remove the `--rm` flag from the run command. This will keep
- longer video take some time to encrypt and decrypt. Be patient.
- Also longer video processing times may require more memory. You can increase the memory limit by adding the `-m` flag

✅ Now you can manually select videos from the GUI and encrypt them inside the Docker container!
