package com.iflytek;

import com.iflytek.cloud.speech.RecognizerListener;
import com.iflytek.cloud.speech.RecognizerResult;
import com.iflytek.cloud.speech.SpeechConstant;
import com.iflytek.cloud.speech.SpeechError;
import com.iflytek.cloud.speech.SpeechRecognizer;
import com.iflytek.cloud.speech.SpeechSynthesizer;
import com.iflytek.cloud.speech.SpeechUtility;
import com.iflytek.cloud.speech.SynthesizerListener;

public class SRTest {
    private static final String APPID = "5327d7bb";
    private static final String DOMAIN = "iat";
    private static final String LANGUAGE = "zh_cn";
    private static final String ACCENT = "mandarin";
    
    private RecognizerListener mRecoListener = new RecognizerListener() {
        
        public void onVolumeChanged(int volume) {
            if (volume > 0)
                DebugLog.Log("*************音量值:" + volume + "*************");
            
        }
        
        public void onResult(RecognizerResult result, boolean isLast) {
            DebugLog.Log("Result:"+result.getResultString());
        }
        
        public void onEvent(int eventType, int arg1, int arg2, String msg) {
            // TODO Auto-generated method stub
            
        }
        
        public void onError(SpeechError error) {
            error.getErrorDescription(true);
        }
        
        public void onEndOfSpeech() {
            DebugLog.Log("结束:" );
            
        }
        
        public void onBeginOfSpeech() {
            DebugLog.Log("*************开始录音*************");
            
        }
    };
    
    private SynthesizerListener mSynListener = new SynthesizerListener() {
        
        public void onSpeakResumed() {
            DebugLog.Log("继续播放:" );            
        }
        
        public void onSpeakProgress(int arg0, int arg1, int arg2) {
            
        }
        
        public void onSpeakPaused() {
            DebugLog.Log("播放暂停:" );            
        }
        
        public void onSpeakBegin() {
            DebugLog.Log("speak start");
        }
        
        public void onCompleted(SpeechError error) {
            if(error == null){
                DebugLog.Log("播放完成");
            }else{
                DebugLog.Log("播放错误" + error.getErrorDesc());
            }
            
        }
        
        public void onBufferProgress(int arg0, int arg1, int arg2, String arg3) {
            // TODO Auto-generated method stub
            
        }
    };
    
    public void robotSpeak(String msg){
        DebugLog.Log("pre speak:"+msg);
       // if (SpeechSynthesizer.getSynthesizer() == null) {
            SpeechSynthesizer mTts = SpeechSynthesizer.createSynthesizer();
            mTts = SpeechSynthesizer.getSynthesizer();
            mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_CLOUD);
            mTts.setParameter(SpeechConstant.VOICE_NAME, "xiaoyan");
            mTts.setParameter(SpeechConstant.SPEED, "50");
            mTts.setParameter( SpeechConstant.TTS_AUDIO_PATH, "./temp.pcm" );
          //设置音调
            mTts.setParameter(SpeechConstant.PITCH, "50");
            //设置音量
            mTts.setParameter(SpeechConstant.VOLUME, "50");
            //设置播放器音频流类型
            mTts.setParameter(SpeechConstant.STREAM_TYPE, "3");
            DebugLog.Log("set param done");
            mTts.startSpeaking(msg,mSynListener);
        //}
    }
    
    
    
    public void recognizeOrder() {
        if (SpeechRecognizer.getRecognizer() == null) {
            SpeechRecognizer mIat = SpeechRecognizer.createRecognizer();
            mIat.setParameter(SpeechConstant.DOMAIN, DOMAIN);
            mIat.setParameter(SpeechConstant.LANGUAGE, LANGUAGE);
            mIat.setParameter(SpeechConstant.ACCENT, ACCENT);
            
            mIat.startListening(mRecoListener);
        }
    }
    
    
    public static void main(String[] args) {
        SpeechUtility.createUtility("appid=" + APPID);
        SRTest srtest = new SRTest();
        //srtest.recognizeOrder();
        srtest.robotSpeak("我叫树莓派一号，是一个机器人");
    }
}
