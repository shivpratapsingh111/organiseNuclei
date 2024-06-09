This script moves unwanted nuclei templates to a different directory, so they don't get executed while you use nuclei, You can get them back whenever you want using `-rev` flag.
---
### Exclude Nuclei Templates based on IDs
 
- organiseNuclei.py - Main script

- id.txt - contains IDs to exclude (You can add more IDs to exclude)

- .separated/ - Output directory. (Hidden in linux)

### Usage:

- `--help`: List available options

    ```
    python3 organiseTemplates.py --help
    ```

- `No flag provided`: Works on default values (directory: /home/$user/nuclei-templates, file: Default array in script)

    ```
    python3 organiseTemplates.py
    ```

- ` -dir -f id.txt`: Provide custom file to match IDs from

    ```
    python3 organiseTemplates.py -dir /home/nuclei-templates -i id.txt
    ```

- `-dir /home/nuclei-templates/`: Provide custom path for nuclei templates

    ```
    python3 organiseTemplates.py -dir /home/nuclei-templates
    ```

- `-rev`: It will move back all the template files to their orgin path. 
    
    ```
    python3 organiseTemplates.py -rev
    ```


**Currently it only supports exclusion through IDs**

<!--### Workflow:

- Retrives ID from file and if **-f** flag provided, else uses predefined array with IDs
- Makes **.separated/** directory (hidden in linux)
- It matches id (string) with `id:` scalar in each and every template in provided directory and it's sub directory.
- Moves templates with matched id to **.separated/** directory
- Notes down it's path in **.config** file under **.separated/** dir
--> 
 
### TODO

- [ ] Add support to exclusion through tags
- [ ] Implement multithreading
- [x] Add flag to get back removed templates

---

## Open for contributions