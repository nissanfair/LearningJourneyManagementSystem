console.log("skills.js load!");
const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      skillName: "",
      skillDesc: "",
      disabled: false,
      message: "",
      skills: "", // Placeholder for now it is to hold all the skills coming from the back end
    };
  },
  methods: {
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
          url = "http://localhost:5000/skill/" + id + "/softdelete";
          axios
            .get(url)
            .then((response) => {
              // process response.data object
              stat = response.data.code;
              if (stat) {
                Swal.fire({
                  title: "Deleted!",
                  text: "Skill has been deleted.",
                  icon: "success",
                  allowOutsideClick: false,
                }).then((result) => {
                  if (result.isConfirmed) {
                    //refresh the page
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
      this.skillDesc = "";
      this.skillName = "";
    },
    create() {
      this.disabled = true;

      //Axios post
      url = "http://localhost:5000/skill";
      //check if fields are not empty
      if (this.skillName.length == 0 || this.skillDesc.length == 0) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "All fields must be filled up!",
        });

        this.disabled = false;
      } else {
        axios
          .post(url, {
            skill_name: this.skillName,
            skill_desc: this.skillDesc,
          })
          .then((response) => {
            // process response.data
            console.log("create response:" + response.data.code);
            stat = response.data.code;
            if (stat) {
              Swal.fire({
                title: "Created!",
                text: "Skill has been created.",
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

            //When skill already exists
            if (error.response.status) {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Skill already Exists!",
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
  },
  created() {
    url = "http://localhost:5000/skill";
    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data.code);
        if (response.data.code == 200) {
          this.skills = response.data.data.skills;
        }
        //When all skills are softdeleted
        else {
          this.message = "<p>There are no skills currently available</p>";
        }
      })
      .catch((error) => {
        // process error object
        console.log(error.response.status);
        //When skills database is empty
        if (error.response.status == 404) {
          this.message = "<p> There is currently no skills created </p>";
        }
      });
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");
