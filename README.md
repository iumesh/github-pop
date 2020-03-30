### About project
    
CLI app that prints the most popular repos of given organization and their top contributors

### To run app

1. Add `.env` file where app.py is        
    
    Copy paste following
    ```
    GITHUB_USERNAME="#######"
    GITHUB_PASSWORD="#######"
    ```        
       
    Add your github username and password above in place of hash
            
            
2. Run following command to

    ```bash
    pip3 install -r requirements.txt 
    ```
    
3. To run app 
    ```bash
    # prints 5 popular google repos based on fork and their 3 most contributing contributors
    python3 app.py google 5 3

 
    # to get help
    python3 app.py -h
    ```