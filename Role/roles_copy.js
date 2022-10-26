console.log("roles_copy.js load!");
var skill_name = "";
var this_holder = "";//to hold "this" variable in axios, 
//basically a global variable so that the json object can be accessed outside of the axios function scope

const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      jobrole_name: "",
      jobrole_desc: "",
      disabled: false,
      message: "",
      jobroles: "", // Placeholder for now it is to hold all the roles coming from the back end
      cJobRoleID: "", //this will contain the current jobrole ID that we are going to update
      jobroleSkills: [], //this will contain the list of skills mapped to the current jobrole (aka skills that can help you obtain this jobrole)
      skills: [], //this will contain all the skills
      selectionInput: "", //this will contain the user selecton input from the course drop down list
    };
  },
  methods: {
    retrieve(id) {
      this.cJobRoleID = id;
      //We will try to obtain the current skill name , desc & if any jobrole skill mapping exists
      jobroleUrl = "http://localhost:5000/jobrole/" + id;
      skillUrl = "http://localhost:5000/skill";
      
      //This is to get the current jobroleskills mapping
      axios
        .get(jobroleUrl)
        .then((response) => {
          // process response.data object
          console.log(response.data.data);
          this.jobrole_name = response.data.data.jobrole_name;
          this.jobrole_desc = response.data.data.jobrole_desc;

          //Get all the jobroleskills mappping into a list
          let jrs = response.data.data.linked_skills;
          for (let index = 0; index < jrs.length; index++) {
            this.jobroleSkills.push(
              jrs[index].skill_id + "-" + jrs[index].skill_name
            );
          }
          console.log(this.jobroleSkills)
        })
        .catch((error) => {
          // process error object
          console.log(error.status);
        });
        axios
        .get(skillUrl)
        .then((response) => {
          // process response.data object
          console.log(response.data.data.skills);
          this.skills = response.data.data.skills;
        })
        .catch((error) => {
          // process error object
          console.log(response.data);
        });
    },
    del(id) {
      //Confirmation prompt for deletion
      Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      }).then((result) => {
        if (result.isConfirmed) {
          //use axios to pass the data over
          url = "http://localhost:5000/jobrole/" + id + "/softdelete";
          axios
            .get(url)
            .then((response) => {
              // process response.data object
              stat = response.data.code;
              if (stat) {
                Swal.fire({
                  title: "Deleted!",
                  text: "JobRole has been deleted.",
                  icon: "success",
                  allowOutsideClick: false,
                }).then((result) => {
                  if (result.isConfirmed) {
                    //refresh the current page
                    location.reload();
                  }
                });
              } else {
                Swal.fire({
                  icon: "error",
                  title: "Oops...",
                  text: "Something went wrong!",
                });
              }
            })
            .catch((error) => {
              // process error object
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Something went wrong!",
              });
            });
        }
      });
    },
    cancel() {
      this.jobrole_name = "";
      this.jobrole_desc = "";
      this.jobroleSkills = [];
    },
    create() {
      this.disabled = true;

      //Axios post
      url = "http://localhost:5000/jobrole";
      //check if fields are not empty
      if (this.jobrole_name.length == 0 || this.jobrole_desc.length == 0) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "All fields must be filled up!",
        });

        this.disabled = false;
      } else {
        axios
          .post(url, {
            jobrole_name: this.jobrole_name,
            jobrole_desc: this.jobrole_desc,
          })
          .then((response) => {
            // process response.data
            console.log("create response:" + response.data.code);
            stat = response.data.code;
            if (stat) {
              Swal.fire({
                title: "Created!",
                text: "New Job Role has been created.",
                icon: "success",
                allowOutsideClick: false,
  
              }).then((result) => {
                if (result.isConfirmed) {
                  this.disabled = false;
                  //refresh the current page
                  location.reload();
                }
              });
            }
          })
          .catch((error) => {
            // process error object
            this.disabled = false;
            console.log(error.response.status);

            //When jobrole already exists
            if (error.response.status) {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Jobrole already Exists!",
              });
            } else {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Oops Something Went Wrong!",
              });
            }
          });
      }
    },
    remove(id) {
      // this is to remove the skills in our this.jobroleSkills based on the users input
      this.jobroleSkills.splice(id, 1);
    },
    add() {
      //this is to add to our current course selection list this.jobroleSkills
      if (
        this.selectionInput != "" &&
        !this.jobroleSkills.includes(this.selectionInput)
      ) {
        this.jobroleSkills.push(this.selectionInput);
      }
    },
    update() {
      if(this.jobrole_desc !="" && this.jobrole_name !=""){
      //disable the update button so that they dont spam requests
      this.disabled= true
      //this will handle the submission of changes to the backend
      rUrl = "http://localhost:5000/jobrole/" + this.cJobRoleID;
      rsUrl = "http://localhost:5000/jobrole/" + this.cJobRoleID + "/roleskills";
      let selection = [];
      for (let index = 0; index < this.jobroleSkills.length; index++) {
        selection.push({ jobrole_id: this.jobroleSkills[index].split("-")[0] });
      }
      console.log(selection);

      //first we will update the role name & description
      axios
        .put(rUrl, {
          jobrole_desc: this.jobrole_desc,
          jobrole_name: this.jobrole_name,
        })
        .then(function (response) {
          console.log(response);
          console.log(response.status);
          // Now we will update the roleskills selection
          axios
            .put(rsUrl, {
              roleskills: selection,
            })
            .then(function (response) {
              console.log(response);
              console.log(response.status);
              console.log("update response:" + response.data.code);
              stat = response.data.code;
              if (stat) {
                Swal.fire({
                  title: "Updated!",
                  text: "Job role has been updated.",
                  icon: "success",
                  allowOutsideClick: false,
                }).then((result) => {
                  if (result.isConfirmed) {
                    this.disabled = false;
                    //refresh the current page
                    location.reload();
                  }
                });
              }
            })
            .catch(function (error) {
              console.log(error);
            });
        })
        .catch(function (error) {
          console.log(error);
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Oops There seems to be a duplication in the role Name!",
          });
        });
        //renable the update button
        this.disabled = false
      }
      else{
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Please ensure that Job role Name & Description are not empty!",
        });
        //renable the update button
        this.disabled = false
      }
    },
  },
  created() {
    url = "http://localhost:5000/jobrole";
    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data.code);
        if (response.data.code == 200) {
          this.jobroles = response.data.data.jobroles;
          this_holder = this;
          console.log(this);
          console.log(this_holder);
          for (let i = 0; i < this.jobroles.length; i++) {
            // iterate through roleskills
            for (let j = 0; j < this.jobroles[i].roleskills.length; j++) {
              // get skill id
              skill_id = this.jobroles[i].roleskills[j].skill_id;
              
              // get skill name with skill_id using axios get
              url = "http://localhost:5000/skill/" + skill_id;
              axios
                .get(url)
                .then((response) => {
                  // process response.data object
                  console.log(response.data.code);
                  if (response.data.code == 200) {
                    skill_name = response.data.data.skill_name;
                    console.log(i);
                    console.log(j);
                    console.log(skill_name);
                  }
                })
                .finally(() => {
                  console.log(skill_name);
                  // add skill_name to roleskills
                  console.log(this_holder);
                  this_holder.jobroles[i].roleskills[j].skill_name = skill_name;
                });
  
            }
            
            }
        }
        //When all jobroles are softdeleted
        else {
          this.message = "<p>There are no jobroles currently available</p>";
        }
      })
      .catch((error) => {
        // process error object
        console.log(error.response.status);
        //When jobroles database is empty
        if (error.response.status == 404) {
          this.message = "<p> There is currently no jobroles created </p>";
        }
      });
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");
