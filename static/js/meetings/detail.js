

const deleteMeetingBtn = async() => {
    const result = confirm('정말로 삭제하시겠습니까?');
    if (result) {
        const meetId = document.querySelector("#meetId").value;
        const groupId = document.querySelector("#groupId").value;
        const {data} = await axios.post(`/groups/group/${groupId}/checkAuth/`,{
            meetId
        });

        console.log(data);
        if (data.auth === true) {
            document.deleteMeeting.submit();
        }
        else{
            alert('권한이 없습니다.')
        }
    }
    else {
        return false;
    }
};

