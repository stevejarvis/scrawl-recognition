package com.sajarvis.scrawl.preferences;

import android.app.Activity;
import android.os.Bundle;

/*
 * This settings activity will just load the fragment to display settings.
 */
public class SettingsActivity extends Activity{

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		// All we need to do is add the fragment to the activity.
		getFragmentManager().beginTransaction()
				.replace(android.R.id.content, new SettingsFragment())
				.commit();
	}
}
