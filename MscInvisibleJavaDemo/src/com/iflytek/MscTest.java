package com.iflytek;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import com.iflytek.cloud.speech.DataUploader;
import com.iflytek.cloud.speech.RecognizerListener;
import com.iflytek.cloud.speech.RecognizerResult;
import com.iflytek.cloud.speech.Setting;
import com.iflytek.cloud.speech.SpeechConstant;
import com.iflytek.cloud.speech.SpeechError;
import com.iflytek.cloud.speech.SpeechListener;
import com.iflytek.cloud.speech.SpeechRecognizer;
import com.iflytek.cloud.speech.SpeechSynthesizer;
import com.iflytek.cloud.speech.SpeechUtility;
import com.iflytek.cloud.speech.SynthesizeToUriListener;
import com.iflytek.cloud.speech.UserWords;

public class MscTest {

	private static final String APPID = "5327d7bb";

	private static final String USER_WORDS = "{\"userword\":[{\"name\":\"计算机词汇\",\"words\":[\"随机存储器\",\"只读存储器\",\"扩充数据输出\",\"局部总线\",\"压缩光盘\",\"十七寸显示器\"]},{\"name\":\"我的词汇\",\"words\":[\"槐花树老街\",\"王小贰\",\"发炎\",\"公事\"]}]}";

	private static MscTest mObject;

	private static StringBuffer mResult = new StringBuffer();

	public static void main(String args[]) {

		Setting.showLog(true);
		SpeechUtility.createUtility("appid=" + APPID);
		getMscObj().onLoop();
	}

	private static MscTest getMscObj() {
		if (mObject == null)
			mObject = new MscTest();
		return mObject;
	}

	private void onLoop() {
		try {
			DebugLog.Log("*********************************");
			DebugLog.Log("Please input the command");
			DebugLog.Log("1:音频流听写            2：上传词表           3：无声合成           4：退出  ");

			Scanner in = new Scanner(System.in);
			int command = in.nextInt();

			DebugLog.Log("You input " + command);

			switch (command) {
			case 1:
				Recognize();
				break;
			case 2:
				uploadUserWords();
				break;
			case 3:
				Synthesize();
				break;
			case 4:
				System.exit(0);
				break;
			default:
				onLoop();
				break;
			}
		} catch (Exception e) {
			onLoop();
		}
	}

	// *************************************音频流听写*************************************

	/**
	 * 听写
	 */
	private void Recognize() {
		if (SpeechRecognizer.getRecognizer() == null)
			SpeechRecognizer.createRecognizer();
		try {
            RecognizePcmfileByte();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
	}

	/**
	 * 自动化测试注意要点 如果直接从音频文件识别，需要模拟真实的音速，防止音频队列的堵塞
	 * @throws IOException 
	 */
	public void RecognizePcmfileByte() throws IOException {
		// 1、读取音频文件
		FileInputStream fis = null;
		byte[] voiceBuffer = null;
		try {
			fis = new FileInputStream(new File("./t21.pcm"));
			voiceBuffer = new byte[fis.available()];
			fis.read(voiceBuffer);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				if (null != fis) {
					fis.close();
					fis = null;
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		int hasRead = 0;
		 //while((hasRead = fis.read(voiceBuffer))>0)  {
		// 2、音频流听写
		if (0 == voiceBuffer.length) {
			mResult.append("no audio avaible!");
		} else {
			SpeechRecognizer recognizer = SpeechRecognizer.getRecognizer();
			recognizer.setParameter(SpeechConstant.DOMAIN, "iat");
			recognizer.setParameter(SpeechConstant.LANGUAGE, "zh_cn");
			recognizer.setParameter(SpeechConstant.AUDIO_SOURCE, "-1");
			recognizer.setParameter(SpeechConstant.ASR_AUDIO_PATH,
					"./iflytek.pcm");
			recognizer.startListening(recListener);
			ArrayList<byte[]> buffers = splitBuffer(voiceBuffer,
					voiceBuffer.length, 4800);
			mResult.append("recognizeStream");
			for (int i = 0; i < buffers.size(); i++) {
				// 每次写入msc数据4.8K,相当150ms录音数据
				recognizer.writeAudio(buffers.get(i), 0, buffers.get(i).length);
				try {
					Thread.sleep(150);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			recognizer.stopListening();
			mResult.append("stopListening");
		}
		
		//}
	}

	/**
	 * 将字节缓冲区按照固定大小进行分割成数组
	 * 
	 * @param buffer
	 *            缓冲区
	 * @param length
	 *            缓冲区大小
	 * @param spsize
	 *            切割块大小
	 * @return
	 */
	public ArrayList<byte[]> splitBuffer(byte[] buffer, int length, int spsize) {
		ArrayList<byte[]> array = new ArrayList<byte[]>();
		if (spsize <= 0 || length <= 0 || buffer == null
				|| buffer.length < length)
			return array;
		int size = 0;
		while (size < length) {
			int left = length - size;
			if (spsize < left) {
				byte[] sdata = new byte[spsize];
				System.arraycopy(buffer, size, sdata, 0, spsize);
				array.add(sdata);
				size += spsize;
			} else {
				byte[] sdata = new byte[left];
				System.arraycopy(buffer, size, sdata, 0, left);
				array.add(sdata);
				size += left;
			}
		}
		return array;
	}

	/**
	 * 听写监听器
	 */
	private RecognizerListener recListener = new RecognizerListener() {

		public void onBeginOfSpeech() {
			DebugLog.Log("*************开始录音*************");
		}

		public void onEndOfSpeech() {
			DebugLog.Log("识别结果为:" + mResult.toString());
			mResult.delete(0, mResult.length());

			onLoop();
		}

		public void onVolumeChanged(int volume) {
			if (volume > 0)
				DebugLog.Log("*************音量值:" + volume + "*************");

		}

		public void onResult(RecognizerResult result, boolean islast) {

			mResult.append(result.getResultString());
		}

		public void onError(SpeechError error) {
			DebugLog.Log("*************" + error.getErrorCode()
					+ "*************");
		}

		public void onEvent(int eventType, int arg1, int agr2, String msg) {

		}

	};

	// *************************************无声合成*************************************

	/**
	 * 合成
	 */
	private void Synthesize() {
		SpeechSynthesizer speechSynthesizer = SpeechSynthesizer
				.createSynthesizer();
		// 设置发音人
		speechSynthesizer.setParameter(SpeechConstant.VOICE_NAME, "xiaoyan");
		// 设置语速，范围0~100
		speechSynthesizer.setParameter(SpeechConstant.SPEED, "50");
		// 设置语调，范围0~100
		speechSynthesizer.setParameter(SpeechConstant.PITCH, "50");
		// 设置音量，范围0~100
		speechSynthesizer.setParameter(SpeechConstant.VOLUME, "50");
		// 设置合成音频保存位置（可自定义保存位置），默认保存在“./iflytek.pcm”
		speechSynthesizer.synthesizeToUri("科大讯飞语音合成测试程序 ", "D:/bin/test.pcm",
				synthesizeToUriListener);
	}

	/**
	 * 合成监听器
	 */
	SynthesizeToUriListener synthesizeToUriListener = new SynthesizeToUriListener() {

		public void onBufferProgress(int progress) {
			DebugLog.Log("*************合成进度*************" + progress);

		}

		public void onSynthesizeCompleted(String uri, SpeechError error) {
			if (error == null) {
				DebugLog.Log("*************合成成功*************");
				DebugLog.Log("合成音频生成路径：" + uri);
			} else
				DebugLog.Log("*************" + error.getErrorCode()
						+ "*************");
			onLoop();

		}

	};

	// *************************************词表上传*************************************

	/**
	 * 词表上传
	 */
	private void uploadUserWords() {
		try {
			// 创建数据上传实例
			DataUploader dataUploader = new DataUploader();
			UserWords userwords = new UserWords(USER_WORDS);
			// 用户词表信息需转为utf-8格式的二进制数组
			byte[] datas = userwords.toString().getBytes("utf-8");
			dataUploader.setParameter(SpeechConstant.SUBJECT, "uup");
			dataUploader.setParameter(SpeechConstant.DATA_TYPE, "userword");
			dataUploader.uploadData(uploadListener, "userwords", datas);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * 词表上传监听器
	 */
	SpeechListener uploadListener = new SpeechListener() {

		public void onData(byte[] buffer) {
		}

		public void onCompleted(SpeechError error) {
			if (error == null)
				DebugLog.Log("*************上传成功*************");
			else
				DebugLog.Log("*************" + error.getErrorCode()
						+ "*************");
			onLoop();
		}

		public void onEvent(int eventType, String params) {

		}

	};

}
