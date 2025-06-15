
import tarfile
import yaml
import hashlib

# Define the path to the tar file and the member name
tar_path = 'data.g2b'

with tarfile.open(tar_path, mode='r:gz') as tar:
    member = tar.getmember('./data.yml')
    f = tar.extractfile(member)
    content = f.read().decode('utf-8')
    yaml_data = yaml.safe_load(content)
    
    print(f"--- YAML Data ---")
    print('Secret Token : ' + yaml_data['secret']['token'])
    print('Company Code : ' + str(yaml_data['base']['company_code']))
    print('Company Name : ' + yaml_data['base']['company_name'])
    print('Confirm Code : ' + str(yaml_data['base']['confirm_code']))
    print('Crackdown Level : ' + str(yaml_data['base']['crackdown_level']))
    print('Start Time : ' + yaml_data['base']['start_time'])
    print('End Time : ' + yaml_data['base']['end_time'])
    print('Place Name : ' + yaml_data['base']['place_name'])
    print('Plate Text : ' + yaml_data['base']['plate_text'])
    print('Zone : ' + str(yaml_data['base']['zone']))
    print('Image Count : ' + str(len(yaml_data['image'])))
    print()
    
    for i in range(len(yaml_data['image'])):
        member = tar.getmember(yaml_data['image'][i]['image_path'])
        f = tar.extractfile(member)
        content = f.read()
        sha256_hash = hashlib.sha256(content).hexdigest()
        md5_hash = hashlib.md5(content).hexdigest()
        
        print(f"--- image {i:04} ---")
        print('Capture Time : ' + yaml_data['image'][i]['capture_time'])
        print('Crackdown Level : ' + str(yaml_data['image'][i]['crackdown_level']))
        print('Image Level: ' + str(yaml_data['image'][i]['image_level']))
        print('Image Path : ' + yaml_data['image'][i]['image_path'])
        print('Image Size : ' + str(len(content)))
        print(f"SHA256: {sha256_hash}")
        print(f"MD5: {md5_hash}")
        print()

# %%
