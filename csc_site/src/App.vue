<template>
  <div id="app">
    <div class="container-fluid">
      <div class="shadow">
        <div class="header">TỰ KIỂM TRA Y TẾ VỚI COVID-19</div>
        <div class="counter" v-if="this.current_question<6">
          <div class="mark align-middle inline"></div>
          <div class="text align-middle inline">Hãy trả lời câu hỏi sau</div>
        </div>
        <div class="counter" v-else>
          <div class="mark align-middle inline"></div>
          <div class="text align-middle inline">Kết luận</div>
        </div>
        <!-- Question 01-->
        <div class="content_area" v-bind:style="checkdisplay(1)" id="q1">
          <div class="question">{{ q1_data.q }}</div>
          <div class="radiobox" v-for="(af,index) in q1_data.a" v-bind:key="index">
            <input
              type="radio"
              aria-label="a"
              name="a1"
              v-bind:id="index"
              v-bind:value="index"
              v-model="current_answer"
            />
            <label v-bind:for="index">{{af}}</label>
          </div>
        </div>

        <!-- Question 04-->
        <div class="content_area" v-bind:style="checkdisplay(2)" id="q2">
          <div class="question">Bạn đang ở tỉnh thành nào?</div>
          <div class="radiobox">
            <input type="radio" aria-label="a" name="a2" id="a20" value="0" v-model="danger_city" />
            <label for="a20">Các tỉnh thành chưa có ca nhiễm</label>
          </div>
          <div class="radiobox">
            <input type="radio" aria-label="a" name="a2" id="a21" value="1" v-model="danger_city" />
            <label for="a21">Các tỉnh thành đã có ca nhiễm: Hà Nội, Vĩnh Phúc, Hồ Chí Minh, ...</label>
          </div>
        </div>

        <!-- Question 04-->
        <div class="content_area" v-bind:style="checkdisplay(3)" id="q3">
          <div class="question">Bạn có đang gặp những triệu chứng nào sau đây không?</div>
          <div class="radiobox">
            <input type="radio" aria-label="a" name="a3" id="a30" value="0" v-model="ill" />
            <label for="a30">Không gặp bất kỳ triệu chứng nào đưới đây</label>
          </div>
          <div class="radiobox">
            <input type="radio" aria-label="a" name="a3" id="a31" value="1" v-model="ill" />
            <label for="a31">Ho, sốt, khó thở và đau họng</label>
          </div>
        </div>

        <!-- Question 04-->
        <div class="content_area" v-bind:style="checkdisplay(4)" id="q4">
          <div class="question">Bạn có đang ở diện cách ly cộng đồng không?</div>
          <div class="radiobox">
            <input
              type="radio"
              aria-label="a"
              name="a4"
              id="a40"
              value="0"
              v-model="isolation_status"
            />
            <label for="a40">Có</label>
          </div>
          <div class="radiobox">
            <input
              type="radio"
              aria-label="a"
              name="a4"
              id="a41"
              value="1"
              v-model="isolation_status"
            />
            <label for="a41">Không</label>
          </div>
        </div>

        <!-- Question 04-->
        <div class="content_area" v-bind:style="checkdisplay(5)" id="q5">
          <div class="question">Trong vòng 14 ngày bạn có tiếp xúc nào như dưới đây không?</div>
          <div class="radiobox">
            <input
              type="radio"
              aria-label="a"
              name="a5"
              id="a50"
              value="0"
              v-model="relation_status"
            />
            <label for="a50">Tiếp xúc với bệnh nhân nhiễm COVID-19</label>
          </div>
          <div class="radiobox">
            <input
              type="radio"
              aria-label="a"
              name="a5"
              id="a51"
              value="1"
              v-model="relation_status"
            />
            <label for="a51">Tiếp xúc với người nghi nhiễm COVID-19</label>
          </div>
          <div class="radiobox">
            <input
              type="radio"
              aria-label="a"
              name="a5"
              id="a52"
              value="2"
              v-model="relation_status"
            />
            <label for="a52">Tiếp xúc với người tiếp xúc với người nghi nhiễm COVID-19</label>
          </div>
          <div class="radiobox">
            <input
              type="radio"
              aria-label="a"
              name="a5"
              id="a53"
              value="3"
              v-model="relation_status"
            />
            <label for="a53">Không tiếp xúc đối tượng nào liên quan đến COVID-19</label>
          </div>
        </div>
        <!-- Mess 04-->
        <div class="content_area" v-bind:style="checkdisplay(6)" id="q6">
          <div class="icon-wrapper">
            <img class="icon" src="~/./assets/icon.jpg" />
          </div>
          <div class="last_message">{{this.current_message}}</div>
        </div>

        <div class="control" v-if="this.current_question<6">
          <div class="col-xs-6 inline">
            <button class="cancelbtn" v-on:click="handleCancel">Hủy bỏ</button>
          </div>
          <div class="col-xs-6 inline">
            <button class="nextbtn" v-on:click="handleNext">TIẾP THEO</button>
          </div>
        </div>
        <div class="control_last" v-else>
          <div class="col-xs-12">
            <button class="nextbtn" v-on:click="handleReset">Trả lời lại</button>
          </div>
        </div>
      </div>
      <div class="footer">
        Thông tin trắc nghiệm chỉ mang tính chất tham khảo, hãy liên hệ các cơ quan Y tế để nhận thông tin tư vấn cuối cùng.
        <br />Một sản phẩm của Mì Ai Blog (https://ainoodle.vn). Nội dung trắc nghiệm tham khảo của Báo Thanh niên.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      publicPath: process.env.BASE_URL,
      previous_question: -1,
      isolation_status: -1,
      relation_status: -1,
      danger_city: -1,
      ill: -1,
      current_message: "",
      current_question: 1,
      current_answer: -1,
      q1_data: {
        q: "Bạn có vừa trở về từ nước ngoài không?",
        a: [
          "Không tôi chỉ ở Việt Nam",
          "Tôi trở về từ Trung Quốc",
          "Tôi trở về từ Hàn Quốc",
          "Tôi trở về từ Châu Âu, Mỹ",
          "Trở về từ các nước ASEAN",
          "Trở về từ các quốc gia khác"
        ]
      },
      message_list: [
        "Bạn trở về từ nước ngoài. Do đã có triệu chứng nên bạn cần được cách ly điều trị tại cơ sở y tế",
        "Bạn trở về từ nước ngoài. Dù không có các triệu chứng nhưng bạn vẫn cần được cách ly tập trung, theo dõi sức khoẻ trong vòng 14 ngày",
        "Bạn trở về từ nước ngoài. Thực hiện khai báo y tế. Cách ly, giám sát y tế tại gia đình, doanh nghiệp, cơ sở lưu trú, giám sát theo nhóm",
        "Bạn chỉ ở Việt Nam và ở tỉnh/thành không có dịch. Tuy nhiên bạn có triệu chứng ho sốt nên bạn hãy bình tĩnh, đeo khẩu trang và hạn chế tiếp xúc với mọi người. Gọi cho đường dây nóng 19003228 hoặc 19009095 để được tư vấn, khám và điều trị. ",
        "Bạn chỉ ở Việt Nam và ở tỉnh/thành không có dịch. Hiện chưa có triệu chứng gì, bạn hãy phòng bệnh theo khuyến cáo của Bộ Y tế. ",
        "Bạn ở tỉnh/thành có dịch và đang ở khu vực cách ly cộng đồng. Tuân thủ đúng các quy định về cách ly của cơ quan chức năng.",
        "Bạn ở tỉnh/thành có dịch. Do đã tiếp xúc gần với bệnh nhân và có triệu chứng nên bạn cần được cách ly điều trị tại cơ sở y tế ",
        "Bạn ở tỉnh/thành có dịch. Do đã tiếp xúc gần với người nghi nhiễm nên bạn cần bạn cần được cách ly tập trung, theo dõi sức khỏe",
        "Bạn ở tỉnh/thành có dịch. Do đã tiếp xúc gần với người tiếp xúc với người nghi nhiễm nên bạn cần được cách ly tại nhà. Hãy tuân thủ các quy định về cách ly của cơ quan chức năng",
        "Bạn ở tỉnh/thành có dịch. Hiện chưa có triệu chứng gì, bạn hãy phòng bệnh theo khuyến cáo của Bộ Y tế.",
        "Bạn ở tỉnh/thành có dịch. Bạn không tiếp xúc với các nguồn liên quan nhưng bạn có triệu chứng ho sốt nên bạn hãy bình tĩnh, đeo khẩu trang và hạn chế tiếp xúc với mọi người. Gọi cho đường dây nóng 19003228 hoặc 19009095 để được tư vấn, khám và điều trị. "
      ]
    };
  },
  methods: {
    checkdisplay: function(index) {
      if (index === this.current_question) {
        //console.log("Bang")
        return { display: "block" };
      } else {
        //console.log("Khac")
        return { display: "none" };
      }
    },
    handleCancel: function() {
      this.current_message = "Bạn đã hủy trắc nghiệm";
      this.showmessage();
    },

    handleReset: function() {
      this.isolation_status = -1;
      this.relation_status = -1;
      this.danger_city = -1;
      this.ill = -1;
      this.current_message = "";
      this.current_question = 1;
      this.current_answer = -1;
    },

    showmessage() {
      //alert(this.current_message);
      this.current_question = 6;
    },

    handleNext: function() {
      if (this.current_question <= 5)
        if (this.current_question == 1) {
          // Hỏi về nước ngoài về -----------------------------------------
          // Check cau hoi
          if (this.current_answer == -1) {
            alert("Hãy chọn một câu trả lời");
            return;
          }
          //console.log(this.current_answer);
          if (1 <= this.current_answer && this.current_answer <= 4) {
            this.previous_question = 1;
            this.current_question = 3;
          } else if (this.current_answer == 5) {
            // Các nước an toàn
            this.current_message = this.message_list[2];
            this.showmessage();
          } else {
            // Không đi nc ngoài về
            this.current_question = 2;
            return;
          }
          // Thành phố nhiễm bệnh -------------------------------
        } else if (this.current_question == 2) {
          if (this.danger_city == -1) {
            alert("Hãy chọn một câu trả lời");
            return;
          }
          if (this.danger_city == 0) this.current_question++;
          else {
            this.current_question = 4;
          }

          // Tinh trang suc khoe --------------------------------
        } else if (this.current_question == 3) {
          if (this.ill == -1) {
            alert("Hãy chọn một câu trả lời");
            return;
          }
          // Neu chuyen tu form 1 sang (khai bao nhap canh)

          if (this.previous_question == 1) {
            if (this.ill == 1) {
              // Ốm
              this.current_message = this.message_list[0];
              this.showmessage();
            } else {
              // Không ốm
              this.current_message = this.message_list[1];
              this.showmessage();
            }
            return;
          }
          // Chuyen tu form tiếp xúc
          if (this.previous_question == 5) {
            if (this.ill == 1) {
              // Ốm
              this.current_message = this.message_list[10];
              this.showmessage();
            } else {
              // Không ốm
              this.current_message = this.message_list[9];
              this.showmessage();
            }
            return;
          }

          // Neu o tỉnh thành an toàn
          if (this.danger_city == 0) {
            if (this.ill == 1) this.current_message = this.message_list[3];
            else this.current_message = this.message_list[4];

            this.showmessage();
            // Nếu ở tỉnh thành không an toàn
          } else {
            if (this.ill == 1) {
              this.current_message = this.message_list[6];
              this.showmessage();
            } else {
              this.current_message = this.message_list[7];
              this.showmessage();
            }
          }
          // Có bị cách ly ko ------------------------------
        } else if (this.current_question == 4) {
          if (this.isolation_status == -1) {
            alert("Hãy chọn một câu trả lời");
            return;
          }
          // Có cách ly
          if (this.isolation_status == 0) {
            this.current_message = this.message_list[5];
            this.showmessage();
            return;
          }
          // Không cách ly, chuyển câu tiếp xúc
          else {
            this.current_question = this.current_question + 1;
          }
          // Có tiếp xúc ko ---------------------
        } else if (this.current_question == 5) {
          if (this.relation_status == -1) {
            alert("Hãy chọn một câu trả lời");
            return;
          }
          console.log(this.relation_status);
          // Nếu tiếp xúc bênh nhân
          if (this.relation_status == 0) {
            // Hỏi sức khỏe
            this.current_question = 3;
            // Nếu tiếp xúc nghi ngờ
          } else if (this.relation_status < 3) {
            // Khuyến cáo
            console.log(7 + this.relation_status);
            this.current_message = this.message_list[
              7 + parseInt(this.relation_status)
            ];
            this.showmessage();
            // Nếu khong làm gì
          } else {
            this.previous_question = 5;
            this.current_question = 3;
          }
        }
    }
  }
};
</script>

<style>
body {
  background-color: rgb(235, 235, 235);
  margin-bottom: 20px;
  margin-top: 20px;
}
.icon {
  max-width: 100%;
}
.icon-wrapper {
  text-align: center;
}

.content_area {
  background-color: white;
  padding-bottom: 20px;
}

.header {
  border-radius: 10px 10px 0px 0px;
  background-color: seagreen;
  color: white;
  padding: 20px;
  margin-top: 10px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  font-size: large;
}

.counter {
  background-color: white;
  color: black;
  padding: 10px;
}

.question {
  color: black;
  padding: 10px;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
}

.control {
  color: black;
  padding: 10px;
  display: flex;
  justify-content: space-between;
}

.last_message {
  color: black;
  padding: 10px;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  text-align: center;
}

.control_last {
  color: black;
  padding: 10px;
  text-align: center;
}

.inline {
  display: inline-block;
}

.mark {
  background-color: red;
  width: 5px;
  height: 30px;
}

.text {
  text-align: center;
}

.radiobox {
  padding: 0px 10px;
}

.cancelbtn {
  text-transform: uppercase;
  background-color: lightgray;
  color: gray;
  border: 0px;
  padding: 8px 20px;
  border-radius: 8px;
}

.nextbtn {
  text-transform: uppercase;
  background-color: seagreen;
  color: white;
  border: 0px;
  padding: 8px 20px;
  border-radius: 8px;
}

.shadow {
  box-shadow: 5px 10px #888888;
  border-radius: 10px;
}

.combobox {
  margin-left: 10px;
}

.label {
  margin-top: 10px;
  margin-left: 10px;
}

.footer {
  padding: 10px;
  font-size: x-small;
  text-align: center;
  color: #888888;
}
</style>