console.log("roles.js load!");
const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      jobrole_name: "",
      jobrole_desc: "",
      message: "",
      jobroles: "", // Placeholder for now it is to hold all the roles coming from the back end
    };
  },
  methods: {
    del(id) {
      console.log(id); //check that we got the correct id

      // Soft delete without confirmation, comment it out when fixed sweet alerts.
      /*url = "http://localhost:5000/jobrole/" + id + "/softdelete";
      axios
        .get(url)
        .then((response) => {
          // process response.data object
          alert("Soft deleted! please refresh page to view changes.")
          console.log(response.data.code);
          stat = response.data.code;
          
        })*/

      //Confirmation prompt for deletion
      Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
        allowOutsideClick: false,
      }).then((result) => {
        if (result.isConfirmed) {
          //use axios to pass the data over
          url = "http://localhost:5000/jobrole/" + id + "/softdelete";
          axios
            .get(url)
            .then((response) => {
              // process response.data object
              console.log(response.data.code);
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
    create() {
      console.log(this.jobrole_name);
      console.log(this.jobrole_desc);
      url = "http://localhost:5000/jobrole";
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
            Swal.fire({
              title: "Created!",
              text: "New Job Role Created.",
              icon: "success",
              allowOutsideClick: false,
            }).then((result) => {
              if (result.isConfirmed) {
                //refresh the current page
                location.reload();
              }
            });
            console.log(response.status);
          })
          .catch((error) => {
            // process error object
            console.log(error.response.status);
            Swal.fire("Error!", "Job Role already exists", "error");
          });
      }
    },
    edit() {
      console.log(this.jobrole_name);
      console.log(this.jobrole_desc);
      // url = "http://localhost:5000/jobrole/" + id + "/edit";
      // axios.put(url, {
      //   jobrole_name : this.jobrole_name,
      //   jobrole_desc : this.jobrole_desc
      //   })
      // .then(response => {
      // // process response.data
      // alert("Job Role Created! please refresh to view changes.");
      // console.log(response.status)
      // console.log(data)

      // })
      // .catch(error => {
      // // process error object
      // console.log(error)
      // });
    },
    cancel() {
      this.jobrole_desc = "";
      this.jobrole_name = "";
    }
  },
  created() {
    url = "http://localhost:5000/jobrole";
    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data);
        if (response.data.code == 200) {
          this.jobroles = response.data.data.jobroles;
        }
        else {
          this.message = "<p>There are no skills currently available</p>";
        }
      })
      .catch((error) => {
        // process error object
        this.message = "<p>There are no skills currently available</p>";
      });
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");