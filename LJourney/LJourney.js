console.log("LJourney.js load!");

var staff_id = 1;
// get staff_id from url param
try {
  const urlParams = new URLSearchParams(window.location.search);
  staff_id = urlParams.get("staff_id");
  if (staff_id == null) {
    window.location.href = window.location.href + "?staff_id=" + 1;
  }
} catch (error) {
  console.log(error);
}

const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      lj_name: "",
      lj_id: "",
      current_staff_id: "",
      learningjourneys: "",
      staffs: "",
      disabled: false,
      staff_id: "",
      jobrole_id: "", // Placeholder for now it is to hold all the roles coming from the back end
      ljc_id: "",
      course_id: "",
      course_names: [],
      job_roles: [], //This will hold the selection of job roles
      jobroleselection: "", // this will hold the job role selection from the dropdown list
      linked_skills_list: [], //this will hold the skills linked to the selected job role
      courses_list: [], //this will hold the courses that can help clear a particular skill
      selected_skill_id: "", //this will hold the currently selected skill id 
      skill_courses_list: [],
      skill_id: "",
      orig_lj_name:"",
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
          url = "http://localhost:5000/learningjourney/" + id;
          axios
            .delete(url)
            .then((response) => {
              // process response.data object
              stat = response.data.code;
              if (stat) {
                Swal.fire({
                  title: "Deleted!",
                  text: "Learning Journey has been deleted.",
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
      this.jobroleselection = "";
      this.linked_skills_list = [];
      this.courses_list = []
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

    //this is called when we click add learning journey
    retrieve() {
      document.getElementById("submitbtn").onclick = () => {
        this.createlj();
      }

      this.jobroleselection = "";
      this.job_roles = null;
      this.lj_name = "";
      this.skill_courses_list = [];

      document.getElementById("jobroleselector").disabled = false;
      document.getElementById("staticBackdropLabel").innerHTML = "Create Learning Journey";
      document.getElementById("submitbtn").innerHTML = "Create";


      url = "http://localhost:5000/jobrole";
      axios
        .get(url)
        .then((response) => {
          // handle success
          console.log(response.data.data.jobroles);
          this.job_roles = response.data.data.jobroles;
          console.log(this.job_roles);
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        });
    },
    upd(id) {
      // popup please wait
      Swal.fire({
        title: "Please Wait",
        text: "Loading Learning Journey Details",
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading();
        },
      });
      console.log(id);
      console.log("test update");
      this.retrieve();

      //Axios get
      let url = "http://localhost:5000/learningjourney/" + id;
      
  
      axios
        .get(url)
        .then((response) => {
          

          let learningjourneyobject = response.data.data;
          console.log(learningjourneyobject);

          axios.get(`http://localhost:5000/jobrole/${learningjourneyobject.linked_jobrole.jobrole_id}`)
          .then((response) => {
            console.log(response.data.data);
          });

          this.jobroleselection = learningjourneyobject.jobrole_id;
          this.job_roles = [learningjourneyobject.linked_jobrole];
          this.lj_name = learningjourneyobject.lj_name;
          this.orig_lj_name = learningjourneyobject.lj_name;

          document.getElementById("jobroleselector").disabled = true;
          document.getElementById("staticBackdropLabel").innerHTML = "Update Learning Journey";
          document.getElementById("submitbtn").innerHTML = "Update";

          // close popup
          Swal.close();

          document.getElementById("submitbtn").onclick = () => {
            if (this.skill_courses_list.length == 0 || this.lj_name.length == 0) {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "The Learning Journey name and your course selections must be filled up!",
              });
            } else {
              let url = "http://localhost:5000/learningjourney/" + id;

              axios.get(`http://localhost:5000/learningjourney/name/${this.lj_name}`)
                .then((response) => {
                  // if code is 404, then the learning journey name is not taken
                  if (this.orig_lj_name == this.lj_name || response.data.code == 404) {
                    axios.delete(url).then((response) => {
                      console.log(response.data);
                      console.log(this.lj_name)
                      let course_list = [];
                      for (let courseobject of this.skill_courses_list) {
                        console.log(courseobject);
                        course_list.push(courseobject["courseID"]);
                      }
                      url = "http://localhost:5000/learningjourney"

                      var postObject = {
                        staff_id: parseInt(staff_id),
                        lj_name: this.lj_name,
                        jobrole_id: this.jobroleselection,
                        lj_id: id,
                        courses: course_list
                      }

                      axios
                        .post(url, postObject)
                        .then((response) => {
                          console.log("create response:" + response.data.code);
                          stat = response.data.code;
                          if (stat) {
                            Swal.fire({
                              title: "Updated!",
                              text: "Learning Journey has been updated.",
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
                        });
                    });
                  } else {
                    Swal.fire({
                      icon: "error",
                      title: "Oops...",
                      text: "A Learning Journey with the same name already Exists!",
                    });
                  }
                });
            }



          }
          let newskill_course_list = [];
          for (let courseobject of learningjourneyobject.linked_courses) {
            console.log(courseobject);
            let newcourseobject = { "courseName": courseobject.course_name, "courseID": courseobject.course_id };
            newskill_course_list.push(newcourseobject);
          }
          this.skill_courses_list = newskill_course_list;
          this.obtain();



          //   {
          //     "jobrole_id": 1,
          //     "lj_id": 1,
          //     "lj_name": "LJ to be swe",
          //     "ljcourses": [
          //         {
          //             "course_id": "IS111",
          //             "lj_id": 1,
          //             "ljc_id": 1
          //         }
          //     ],
          //     "staff_id": 1
          // }

        });





    },
    obtain() {
      //here we will try and populate the skills needed for the selected job role
      if (this.jobroleselection != "") {
        url = "http://localhost:5000/jobrole/" + this.jobroleselection;
        axios
          .get(url)
          .then((response) => {
            // handle success
            console.log(response.data.data);
            console.log(response.data.data.linked_skills);
            this.linked_skills_list = response.data.data.linked_skills;
          })
          .catch(function (error) {
            // handle error
            console.log(error);
            this.linked_skills_list = [];
          });
      }
    },
    populate(id) {// here we will populate the table to show the courses to clear a particular selected skill
      this.selected_skill_id = id
      url = "http://localhost:5000/skill/" + id
      axios
        .get(url)
        .then((response) => {
          // handle success
          console.log(response.data.data);
          console.log(response.data.data.linked_courses)
          this.courses_list = response.data.data.linked_courses
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        });

    },
    save(cid, cname) {//here we will save the user selection 
      //first grab the current skillid
      let skillid = this.selected_skill_id

      let course_skill = { skillID: skillid, courseName: cname, courseID: cid };
      let x = true;
      for (let i = 0; i < this.skill_courses_list.length; i++) {
        if (this.skill_courses_list[i].courseID == cid) {
          x = false;
        }
      }
      if (x == true) {
        this.skill_courses_list.push(course_skill);
      }
    },
    remove(index) {
      this.skill_courses_list.splice(index, 1)
    },
    createlj() {


      if (this.skill_courses_list.length == 0 || this.lj_name.length == 0) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "The Learning Journey name and your course selections must be filled up!",
        });
      } else {
        console.log(this.lj_name)
        let course_list = [];
        for (let courseobject of this.skill_courses_list) {
          console.log(courseobject);
          course_list.push(courseobject["courseID"]);
        }
        url = "http://localhost:5000/learningjourney"

        var postObject = {
          staff_id: parseInt(staff_id),
          lj_name: this.lj_name,
          jobrole_id: this.jobroleselection,
          courses: course_list
        }

        axios
          .post(url, postObject)
          .then((response) => {
            console.log("create response:" + response.data.code);
            stat = response.data.code;
            if (stat) {
              Swal.fire({
                title: "Created!",
                text: "New Learning Journey has been created.",
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
                text: "A Learning Journey with the same name already Exists!",
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
    }

  },
  created() {
    // popup please wait
    Swal.fire({
      title: "Please Wait",
      text: "Loading Learning Journey Details",
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });
    this.current_staff_id = staff_id;
    // lets get all the staffs! for the selecting staff_id dropdown :)
    axios.get("http://localhost:5000/staff").then((response) => {
      this.staffs = response.data.data.staffs;
      console.log(this.staffs);
    });

    url = `http://localhost:5000/staff/learningjourney/${staff_id}`;

    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data);
        if (response.data.code == 200) {
          this.learningjourneys = response.data.data.learningjourneys;
          console.log(this.learningjourneys);
          this.lj_name = response.data.data.lj_name;
          this.lj_id = response.data.data.lj_id;
          // close swal loading popup
          Swal.close();
          
        }
      })
      .catch((error) => {
        // process error object
        console.log(error.response.status);
        //When jobroles database is empty
        if (error.response.status == 404) {
          Swal.close();
          this.message =
            "<p> There is currently no learning journey created </p>";
        }
      });
  },
});


// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");
