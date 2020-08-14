import React from 'react';

import LectureVideo from '../../../../components/LectureVideo/LectureVideo';

const lecture = props => (
    <div>
        {props.lecture}
        <LectureVideo userEmail={props.userEmail}
                        userType={props.userType} />
    </div>
);

export default lecture;