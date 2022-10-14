console.log("roles_copy.js load!");
const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      jobrole_name: "",
      jobrole_desc: "",
      message: "",
      disabled: false,
      roleImg: "",
      jobroles: "", // Placeholder for now it is to hold all the roles coming from the back end
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
        }
        //When all jobroles are softdeleted
        else {
          this.message = "<p>There are no jobroles currently available</p>";
        }
      })
      .catch((error) => {
        // process error object
        this.message = "<p>There are no roles currently available</p>";
        })
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");