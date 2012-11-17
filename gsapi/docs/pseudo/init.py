Pyseudo Initialize

Initialize App
	Load Global App Data from data.static *.yaml files
        static:
    		- models  : json
                Cnt:
                  - json for client to post a new doc
              countrys: json
              langs   : json
              locs    : json
              typs    : json
              tags    : json
              tzs     : json
	Create Admin User
	    controllers.App.CreateAdmin # this is initial admin with pw: admin
Initial admin user will login
    TODO: Outline steps involved here
    # If login user and password is permitted without oath tokin
        If user is root.admin, continue, otherwise reject.
OAuth Initialize
    TODO: Outline steps involved here and docs/models involved
    # Create a Client Usr