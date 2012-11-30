package com.sajarvis.scrawl.preferences;

import android.os.Bundle;
import android.preference.PreferenceFragment;

import com.sajarvis.scrawl.R;

/*
 * Fragment just loads preferences resource.
 */
public class SettingsFragment extends PreferenceFragment {
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		addPreferencesFromResource(R.xml.preferences);
	}
}
